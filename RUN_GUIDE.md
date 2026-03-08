# AgIL Website - Hướng Dẫn Sử Dụng & Deploy 🚀

Tài liệu này hướng dẫn chi tiết cách chạy trang web ở máy cá nhân (Local) để kiểm thử, cũng như cách cập nhật nội dung và tự động deploy lên GitHub Pages.

---

## 1. Chạy Trang Web Ở Máy Cá Nhân (Local Development)

Việc chạy trang web ở local giúp bạn xem trước các thay đổi (thêm người, thêm bài báo, đổi giao diện, v.v.) trước khi đưa lên mạng.

### 1.1 Yêu Cầu Cài Đặt Ban Đầu (Chỉ làm 1 lần)
Bạn cần cài đặt Ruby và môi trường làm việc. Nếu chưa có, trên Ubuntu/Linux hãy chạy lệnh sau:
```bash
sudo apt update
sudo apt install ruby-full build-essential zlib1g-dev
```

Sau khi cài Ruby, cần cài đặt `bundler` (công cụ quản lý thư viện của Ruby):
```bash
sudo gem install bundler
```

> **🔥 LỖI THƯỜNG GẶP KHÔNG CÓ QUYỀN GHI (PermissionError):** 
> Nếu bạn gặp lỗi *`Bundler::PermissionError`* hoặc lỗi không có quyền ghi vào `/var/lib/gems/`, cấu hình để Bundler cài đặt thư viện vào thẳng thư mục dự án hiện tại bằng lệnh:
> ```bash
> bundle config set --local path 'vendor/bundle'
> ```

### 1.2 Khởi Động Trang Web
Mỗi khi muốn mở web ở máy để xem, bạn mở Terminal tại thư mục code (`/home/viet/Downloads/web` hoặc thư mục dự án) và chạy lệnh:
```bash
bundle install   # Lệnh này đảm bảo tải đầy đủ thư viện Jekyll thiết yếu
bundle exec jekyll serve --livereload
```
*(Nếu làm biếng gõ lệnh dài, bạn có thể chạy file helper tôi đã tạo sẵn: `sh scripts/build_help.sh` - Lưu ý: trong helper này cũng sẽ chạy lệnh `bundle install` tự động).*

### 1.3 Xem Trang Web
Khi Terminal hiện dòng chữ `Server address: http://127.0.0.1:4000/`, hãy mở trình duyệt web và truy cập địa chỉ:
**[http://localhost:4000/](http://localhost:4000/)**
Tính năng `--livereload` giúp trình duyệt tự động tải lại trang mỗi khi bạn lưu file.

---

## 2. Các Bước Cập Nhật Nội Dung Cơ Bản

Hệ thống được thiết kế theo hướng **Data-Driven**. Bạn không cần sửa giao diện (HTML), chỉ cần sửa thư mục Data.

### 2.1 Cập Nhật Bài Báo (Publications)
Mở file `_data/publications.yml` và thêm vào danh sách theo mẫu.
```yaml
- title: "Interpretable Landslide Risk Assessment via Machine Learning and Explainable AI"
  authors: "Nguyen, Duc Quang-Anh and Vu, Ha Phuong and Le, Ba Tung Duong and Mai, Hanh Thi and Thanh, Hoa Do"
  year: 2025
  type: "conference" # hoặc "journal"
  venue: "Proceedings of the International Student Science Forum"
  thumbnail: "assets/images/publications/landslide.jpg"
  paper_link: "https://example.com/paper/landslide-risk-2025"
```

### 2.2 Thêm Hoặc Sửa Thông Tin Thành Viên (People)
Mọi thông tin thành viên đều được lưu trong thư mục `_people/`.
Để thêm người mới, tạo một file Markdown (`.md`) mới trong thư mục này với nội dung theo mẫu:
```markdown
---
layout: person
title: Lê Minh Việt
job_title: Research Assistant
role_group: Research Assistants      # Các nhóm cố định: Executive Board, Research Assistants, Interns, Alumni 
order: 2                             # Thứ tự hiển thị 
email: 24070480@vnu.edu.vn
photo: /assets/images/people/le_minh_viet.jpg
linkedin: https://www.linkedin.com/in/vi%E1%BB%87t-lee-821500329/
github: https://github.com/Vlet0
scholar: 
---

Le Minh Viet was born in Hanoi, Vietnam, in 2006. He is currently pursuing a degree in Financial Technology...
*(Phần giới thiệu chi tiết viết ở đây)*
```
Đừng quên lưu hình đại diện của họ vào thư mục `assets/images/people/`.

### 2.3 Thêm Tin Tức Tức (Recent News & Activities)
Mở file `_data/news.yml` và thêm những file đầu tiên:
```yaml
- title: "AgIL Welcomes New Interns"
  date: "2026-01-20"
  content: "We are thrilled to welcome a new cohort of research interns joining us for the spring semester."
```
Trang chủ sẽ tự động hiển thị 10 bài báo mới nhất và chia trang (Pagination) ở các trang tiếp theo.

---

## 3. Hoạt Động & Triển Khai Lên GitHub Pages (Deploy)

Website của bạn đã được kết nối và cấu hình hoàn tất với kho lưu trữ GitHub tại:
**[https://github.com/agorala-b/OurWeb](https://github.com/agorala-b/OurWeb)**

Bạn không cần tự build và copy các file tĩnh lên mạng. GitHub Actions sẽ làm tự động giúp bạn.

### Các Bước Thực Hiện Deploy:
1. **Sửa code hoặc cập nhật Data ở máy local.**
2. **Kiểm tra ở Local** bằng lệnh `sh scripts/build_help.sh` đảm bảo giao diện hiển thị đúng ý.
3. **Commit & Push** các thay đổi đó lên nhánh chính để tự động public:
   ```bash
   git add -A
   git commit -m "Cập nhật bài báo mới trên ResearchGate"
   git push origin migration/github-pages-ui-modern  
   ```
   *(Lưu ý: Nếu bạn có thể sát nhập nhánh `migration/github-pages-ui-modern` này vào nhánh `main` (hoặc `master`) trên GitHub, thì về sau bạn chỉ cần push thay đổi lên `main` là GitHub Pages sẽ tự động Build trang web)*.

### Quá Trình Build Trên GitHub Chạy Như Thế Nào?
- Sau khi bạn push code lên GitHub, một hệ thống gọi là **GitHub Actions** (được định nghĩa trong file `.github/workflows/deploy.yml`) sẽ được kích hoạt ẩn.
- Quá trình này tự build phiên bản Jekyll mới nhất khoảng vài phút, sau đó nó sẽ publish trang web vào nhánh `gh-pages` hoặc lên link chính thức của tổ chức.
- Bạn có thể vào mục **Actions** trên Repository GitHub để theo dõi xem quá trình Deploy đã thành công hay xảy ra lỗi (dấu tích xanh ✅).
