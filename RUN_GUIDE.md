# AgIL Website - Hướng Dẫn Sử Dụng & Quản Trị 

Tài liệu này hướng dẫn cách vận hành, cập nhật nội dung và triển khai trang web **AgIL (Agora Intelligence Lab)** từ máy cá nhân lên GitHub.

---

## 1. Chạy Trang Web Ở Máy Cá Nhân (Local Development)

Trước khi công khai thay đổi, bạn nên chạy thử ở máy local để kiểm tra giao diện.

### 1.1 Cài đặt môi trường (Chỉ làm một lần)
Đảm bảo máy đã cài Ruby và Bundler. Trên Linux/Ubuntu:
```bash
sudo apt update
sudo apt install ruby-full build-essential zlib1g-dev
sudo gem install bundler
```

Nếu gặp lỗi về quyền ghi (permission), cấu hình cài thư viện vào thư mục dự án:
```bash
bundle config set --local path 'vendor/bundle'
```

### 1.2 Khởi động server
Mở Terminal tại thư mục dự án và chạy:
```bash
bundle install   # Cài đặt/cập nhật thư viện cần thiết
bundle exec jekyll serve --livereload
```
*(Hoặc dùng script hỗ trợ: `sh scripts/build_help.sh`)*

Truy cập trang web tại: **[http://localhost:4000](http://localhost:4000)**

---

## 2. Hướng Dẫn Cập Nhật Nội Dung (Data-Driven)

Hệ thống được thiết kế để bạn chỉ cần cập nhật dữ liệu trong các file cấu hình mà không cần sửa code HTML phức tạp.

### 2.1 Thêm Tin Tức (News)
Mở file `_data/news.yml`. Thêm tin mới lên **đầu file** để nó hiện ra đầu tiên:
```yaml
- title: "Tiêu đề tin tức..."
  date: "YYYY-MM-DD"
  content: "Nội dung chi tiết của bản tin..."
```

### 2.2 Thêm Bài Báo (Publications)
Mở file `_data/publications.yml`. Thêm thông tin theo mẫu:
```yaml
- title: "Tên bài báo khoa học"
  authors: "Tên các tác giả"
  year: 2026
  type: "journal" # hoặc "conference"
  venue: "Tên tạp chí/hội thảo"
  thumbnail: "assets/images/publications/ten_anh.jpg" # Ảnh minh họa
  paper_link: "https://doi.org/..." # Link tải/xem bài báo
```
*Lưu ý: Ảnh thumbnail nên lưu vào thư mục `assets/images/publications/`.*

### 2.3 Quản Lý Thành Viên (People)
Mỗi thành viên có một file riêng trong thư mục `_people/`.
Để thêm người mới, hãy tạo file `.md` (ví dụ: `nguyen_van_a.md`):
```markdown
---
layout: person
title: Nguyễn Văn A
job_title: Research Assistant
role_group: Member # Nhóm: Executive Board, Member, Interns, Alumni 
order: 1 # Thứ tự hiển thị trong nhóm
photo: /assets/images/people/nguyen_van_a.jpg
email: email@vnu.edu.vn
linkedin: https://linkedin.com/in/...
github: https://github.com/...
---
Viết tiểu sử hoặc giới thiệu ngắn về thành viên ở đây.
```

### 2.4 Thêm Dataset (Dữ liệu nghiên cứu)
Mở file `_data/datasets.yml`. Thêm thông tin tập dữ liệu:
```yaml
- name: "Tên tập dữ liệu"
  description: "Mô tả ngắn gọn về dữ liệu"
  domain: "Lĩnh vực (VD: NLP, Computer Vision)"
  format: "Định dạng (VD: CSV, JSON)"
  size: "Dung lượng (VD: 100 MB)"
  license: "Giấy phép (VD: MIT, CC BY 4.0)"
  download_link: "/assets/datasets/data.zip" # Để trống "" nếu hiện "Coming Soon"
```

---

## 3. Triển Khai Lên GitHub Pages (Deploy)

Khi đã ưng ý với các thay đổi ở máy local, bạn dùng các lệnh sau để đẩy lên GitHub:

```bash
# 1. Gom tất cả thay đổi
git add .

# 2. Tạo ghi chú thay đổi
git commit -m "Cấu trúc lại dữ liệu và cập nhật nội dung mới"

# 3. Đẩy lên nhánh main (Lệnh này sẽ kích hoạt GitHub Actions tự build web)
git push origin main
```

**Kiểm tra trạng thái:**
Vào mục **Actions** trên repo GitHub để xem quá trình build. Khi thấy dấu tích xanh ✅, trang web sẽ được cập nhật tại:
**[https://agorala-b.github.io/Agoralab/](https://agorala-b.github.io/Agoralab/)** (hoặc domain riêng của bạn).
