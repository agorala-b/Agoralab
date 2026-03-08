#!/usr/bin/env python3
"""
Kiểm tra links trong publication YAML files.
Lý do: đảm bảo github_link và paper_link có format URL hợp lệ.
Chạy: python3 tests/check_links.py (từ thư mục web/)
Rollback: xoá file này nếu không cần.
"""

import os
import re
import sys
import glob

# Regex kiểm tra URL format cơ bản
URL_PATTERN = re.compile(
    r'^https?://'  # http:// hoặc https://
    r'[a-zA-Z0-9]'  # ít nhất 1 ký tự domain
    r'[a-zA-Z0-9._~:/?#\[\]@!$&\'()*+,;=%-]*$'  # phần còn lại
)


def check_yaml_links(yaml_dir='publications/data'):
    """Đọc tất cả file .yml trong yaml_dir, kiểm tra github_link và paper_link."""
    try:
        import yaml
    except ImportError:
        # Fallback: parse đơn giản nếu không có PyYAML
        print("⚠️  PyYAML không có sẵn, sử dụng regex parser đơn giản.")
        return check_yaml_links_simple(yaml_dir)

    errors = []
    files_checked = 0

    for yml_path in sorted(glob.glob(os.path.join(yaml_dir, '*.yml'))):
        files_checked += 1
        with open(yml_path, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                errors.append(f"❌ {yml_path}: YAML parse error — {e}")
                continue

        if isinstance(data, dict):
            items_to_check = [data]
        elif isinstance(data, list):
            items_to_check = data
        else:
            errors.append(f"❌ {yml_path}: YAML không chứa dict hoặc list hợp lệ")
            continue

        for item in items_to_check:
            if not isinstance(item, dict):
                continue
            for field in ('github_link', 'paper_link'):
                val = item.get(field, '')
                if val and val.strip():
                    if not URL_PATTERN.match(val.strip()):
                        errors.append(f"❌ {yml_path}: {field} = '{val}' — không phải URL hợp lệ")

    return files_checked, errors


def check_yaml_links_simple(yaml_dir='publications/data'):
    """Fallback parser khi không có PyYAML."""
    errors = []
    files_checked = 0
    link_pattern = re.compile(r'^(github_link|paper_link):\s*["\']?(.*?)["\']?\s*$')

    for yml_path in sorted(glob.glob(os.path.join(yaml_dir, '*.yml'))):
        files_checked += 1
        with open(yml_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                m = link_pattern.match(line)
                if m:
                    field, val = m.group(1), m.group(2)
                    if val and not URL_PATTERN.match(val):
                        errors.append(f"❌ {yml_path}:{line_num}: {field} = '{val}' — không phải URL hợp lệ")

    return files_checked, errors


def main():
    yaml_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'publications', 'data')

    if not os.path.isdir(yaml_dir):
        print(f"⚠️  Thư mục {yaml_dir} không tồn tại. Bỏ qua kiểm tra.")
        sys.exit(0)

    files_checked, errors = check_yaml_links(yaml_dir)

    print(f"\n📋 Kiểm tra links trong publication YAML")
    print(f"   Thư mục: {yaml_dir}")
    print(f"   Số file: {files_checked}")

    if errors:
        print(f"\n❌ Tìm thấy {len(errors)} lỗi:\n")
        for err in errors:
            print(f"   {err}")
        sys.exit(1)
    else:
        print(f"\n✅ Tất cả links hợp lệ!")
        sys.exit(0)


if __name__ == '__main__':
    main()
