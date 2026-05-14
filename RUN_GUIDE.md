# AgIL Website - Huong Dan Van Hanh

Tai lieu huong dan quan tri nội dung va trien khai trang web Agora Intelligence Lab (AgIL).

---

## 1. Moi truong phat trien (Local Development)

### 1.1 Cai dat moi truong
Yeu cau: Ruby va Bundler.
```bash
sudo apt update
sudo apt install ruby-full build-essential zlib1g-dev
sudo gem install bundler
bundle config set --local path 'vendor/bundle'
```

### 1.2 Chay server local
Cach nhanh nhat:
```bash
sh scripts/build_help.sh
```

Hoac chay tung buoc:
```bash
bundle install
bundle exec jekyll serve --livereload
```
Truy cap tai: http://localhost:4000

---

## 2. Cap nhat noi dung

### 2.1 Tin tuc (News)
File: `_data/news.yml`
```yaml
- title: "Tieu de..."
  date: "YYYY-MM-DD"
  content: "Noi dung..."
```

### 2.2 Bai bao (Publications)
File: `_data/publications.yml`
```yaml
- title: "Ten bai bao"
  authors: "Tac gia"
  year: 2026
  type: "journal" # hoac "conference"
  venue: "Noi dang tai"
  thumbnail: "assets/images/publications/anh.jpg"
  paper_link: "Link bai bao"
```

### 2.3 Thanh vien (People)
Tao file `.md` trong thu muc `_people/`:
```markdown
---
layout: person
title: Ho ten
job_title: Chuc danh
role_group: Member # Executive Board, Member, Interns, Alumni 
order: 1
photo: /assets/images/people/anh.jpg
email: email@vnu.edu.vn
---
Tieu su tom tat tai day.
```

### 2.4 Tap du lieu (Datasets)
File: `_data/datasets.yml`
```yaml
- name: "Ten dataset"
  description: "Mo ta"
  domain: "Linh vuc"
  download_link: "/assets/datasets/data.zip"
```

### 2.5 Doi tac (Partners)
File: `_data/partners.yml`
```yaml
- name: "Ten doi tac"
  logo: "/assets/images/partner/logo.png"
```

---

## 3. Git Workflow & Deploy

### 3.1 Day thay doi len nhanh Main
```bash
git add .
git commit -m "Mo ta thay doi"
git pull --rebase origin main
git push origin main
```

### 3.2 Cap nhat dong bo cac nhanh (Sync Branches)
```bash
# Cap nhat nhanh migration tu main
git checkout migration/github-pages-ui-modern
git merge main
git push origin migration/github-pages-ui-modern

# Quay lai nhanh main
git checkout main
```

### 3.3 Kiem tra trien khai
Theo doi tab Actions tren GitHub. Khi thanh cong, trang web se duoc cap nhat tai:
URL: https://agorala-b.github.io/Agoralab/
