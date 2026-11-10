import os
import re
import shutil
import yaml
import markdown
import liquid
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SITE_DIR = os.path.join(BASE_DIR, '_site')

def parse_frontmatter(text):
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1]) or {}
            body = parts[2]
            return fm, body
    return {}, text

def build_site():
    print("[*] Building site into _site/ ...")
    if os.path.exists(SITE_DIR):
        shutil.rmtree(SITE_DIR)
    os.makedirs(SITE_DIR, exist_ok=True)

    # Copy assets
    assets_src = os.path.join(BASE_DIR, 'assets')
    if os.path.exists(assets_src):
        shutil.copytree(assets_src, os.path.join(SITE_DIR, 'assets'))

    # Load config
    config_file = os.path.join(BASE_DIR, '_config.yml')
    config = {}
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

    site_data = {}
    data_dir = os.path.join(BASE_DIR, '_data')
    if os.path.exists(data_dir):
        for f in os.listdir(data_dir):
            if f.endswith(('.yml', '.yaml')):
                key = os.path.splitext(f)[0]
                with open(os.path.join(data_dir, f), 'r', encoding='utf-8') as fp:
                    site_data[key] = yaml.safe_load(fp) or []

    # Load people collection
    people = []
    people_dir = os.path.join(BASE_DIR, '_people')
    if os.path.exists(people_dir):
        for f in os.listdir(people_dir):
            if f.endswith('.md'):
                slug = os.path.splitext(f)[0]
                with open(os.path.join(people_dir, f), 'r', encoding='utf-8') as fp:
                    fm, body = parse_frontmatter(fp.read())
                    fm['slug'] = slug
                    fm['url'] = f"/people/{slug}.html"
                    fm['content_md'] = body
                    people.append(fm)

    # Setup Liquid environment
    env = liquid.Environment()

    def filter_relative_url(val):
        if val is None:
            return ''
        s = str(val).strip()
        if not s.startswith('/'):
            s = '/' + s
        if s.startswith('/Agoralab/'):
            s = s[len('/Agoralab'):]
        return s

    def filter_absolute_url(val):
        return 'http://localhost:4000' + filter_relative_url(val)

    def filter_where(items, key, val):
        if not items:
            return []
        res = []
        for it in items:
            if isinstance(it, dict) and str(it.get(key, '')).strip().lower() == str(val).strip().lower():
                res.append(it)
        return res

    def filter_sort(items, key=None):
        if not items:
            return []
        if key:
            return sorted(items, key=lambda x: str(x.get(key, '')) if isinstance(x, dict) else str(x))
        return sorted(items)

    def filter_reverse(items):
        if not items:
            return []
        return list(reversed(items))

    def filter_markdownify(val):
        return markdown.markdown(str(val or ''))

    env.filters['relative_url'] = filter_relative_url
    env.filters['absolute_url'] = filter_absolute_url
    env.filters['where'] = filter_where
    env.filters['sort'] = filter_sort
    env.filters['reverse'] = filter_reverse
    env.filters['markdownify'] = filter_markdownify

    # Load layouts
    layouts = {}
    layouts_dir = os.path.join(BASE_DIR, '_layouts')
    if os.path.exists(layouts_dir):
        for f in os.listdir(layouts_dir):
            if f.endswith('.html'):
                name = os.path.splitext(f)[0]
                with open(os.path.join(layouts_dir, f), 'r', encoding='utf-8') as fp:
                    fm, body = parse_frontmatter(fp.read())
                    layouts[name] = {'fm': fm, 'body': body}

    def render_with_layouts(layout_name, page_context, content=''):
        ctx = dict(page_context)
        ctx['content'] = content

        if not layout_name or layout_name not in layouts:
            return content

        cur_layout = layouts[layout_name]
        template = env.from_string(cur_layout['body'])
        rendered = template.render(**ctx)

        parent_layout = cur_layout['fm'].get('layout')
        if parent_layout and parent_layout != layout_name:
            return render_with_layouts(parent_layout, page_context, rendered)
        return rendered

    site_obj = {
        'title': config.get('title', 'AgIL'),
        'description': config.get('description', ''),
        'baseurl': '',
        'url': 'http://localhost:4000',
        'data': site_data,
        'people': people,
        'time': '2026'
    }

    # Render top-level pages
    for f in os.listdir(BASE_DIR):
        if f.endswith('.html') and not f.startswith('_'):
            page_path = os.path.join(BASE_DIR, f)
            with open(page_path, 'r', encoding='utf-8') as fp:
                fm, body = parse_frontmatter(fp.read())
            
            page_ctx = {
                'site': site_obj,
                'page': {**fm, 'url': '/' + ('' if f == 'index.html' else f)},
            }
            body_rendered = env.from_string(body).render(**page_ctx)
            final_html = render_with_layouts(fm.get('layout', 'default'), page_ctx, body_rendered)
            
            out_file = os.path.join(SITE_DIR, f)
            with open(out_file, 'w', encoding='utf-8') as fp:
                fp.write(final_html)
            print(f"  -> Generated {f}")

    # Render people individual pages
    out_people_dir = os.path.join(SITE_DIR, 'people')
    os.makedirs(out_people_dir, exist_ok=True)
    for p in people:
        html_body = markdown.markdown(p.get('content_md', ''))
        page_ctx = {
            'site': site_obj,
            'page': p
        }
        final_html = render_with_layouts(p.get('layout', 'person'), page_ctx, html_body)
        out_file = os.path.join(out_people_dir, f"{p['slug']}.html")
        with open(out_file, 'w', encoding='utf-8') as fp:
            fp.write(final_html)

    print(f"  -> Generated {len(people)} people pages")
    print("[*] Build completed successfully!")

class AgilRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE_DIR, **kwargs)

    def do_GET(self):
        if self.path.startswith('/Agoralab'):
            new_path = self.path[len('/Agoralab'):]
            if not new_path:
                new_path = '/'
            self.path = new_path
        return super().do_GET()

def run_server(port=4000):
    server = HTTPServer(('127.0.0.1', port), AgilRequestHandler)
    print(f"[*] Server running at http://localhost:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopping server.")
        server.server_close()

if __name__ == '__main__':
    build_site()
    port = 4000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run_server(port)
