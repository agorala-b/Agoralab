# Migration & UI Modernization Guide: AgIL 🚀

Tài liệu này tổng hợp toàn bộ các thay đổi trong việc chuyển đổi site tĩnh, cấu trúc lại dữ liệu và nâng cấp giao diện UI/UX cho Agora Intelligence Lab (AgIL) chạy trên GitHub Pages.

## 1. Danh sách file thay đổi & thêm mới

**Thêm mới (Thư mục & File):**
- `_config.yml` và `Gemfile`: Cấu hình Jekyll cho GitHub Pages.
- `_layouts/default.html`, `home.html`, `people_index.html`, `person.html`, `publications.html`: Các template chính.
- `_data/news.yml`, `_data/publications.yml`: Nguồn dữ liệu (Data-driven).
- `_people/`: Thư mục Markdown chứa thông tin của từng thành viên (Jekyll Collection).
- `assets/css/agil-modern.css`: Stylesheet chứa CSS Variables và các class (prefix `agil-`).
- `assets/js/nav.js`, `pagination.js`, `gallery.js`: Script xử lý UI (Menu, Lightbox, Pagination).
- `scripts/migrate_data.py`: Script Python dùng để chuyển đổi dữ liệu từ member cũ sang Markdown (đã chạy thành công).
- `scripts/build_help.sh`: Helper để chạy ứng dụng local.
- `.github/workflows/deploy.yml`: Automation pipeline build Jekyll tự động bằng GitHub Actions.
- `backup_original/`: Chứa toàn bộ HTML gốc đã được backup an toàn.

**Sửa đổi/Thay thế:**
- `index.html`, `people.html`, `publications.html`, `datasets.html`, `pics.html`: Chuyển sang format mới dùng Jekyll Front-matter.
- Xóa các trang tĩnh cũ (vì đã tích hợp vào structure mới hoặc không dùng tới theo yêu cầu).

---

## 2. Hướng dẫn Deploy & Rollback

### 2.1. Cập nhật và Deploy tự động (Khuyên dùng)
Source code hiện nay đã được cấu hình GitHub Actions (`.github/workflows/deploy.yml`).
1. Khi có cập nhật mới (Thêm người, thêm bài báo, đổi thông tin), bạn chỉ cần **Commit và Push** code lên nhánh `main` (hoặc `master`).
2. GitHub Actions sẽ tự động kích hoạt `jekyll build` và publish trang web lên GitHub Pages. Không cần chạy thủ công.

### 2.2. Build và Test ở Local
Để xem trang ở máy cá nhân trước khi push:
1. Đảm bảo đã cài `ruby` và `bundler` (VD: `sudo apt install ruby-bundler`).
2. Chạy helper script: `sh scripts/build_help.sh`
3. Truy cập địa chỉ `http://localhost:4000/`.

### 2.3. Rollback
Nếu xảy ra lỗi nghiêm trọng và muốn quay lại phiên bản nguyên thủy:
- Cách 1: Checkout lại commit trước khi làm branch migration này: `git checkout main` (nếu đang ở branch migration) hoặc `git revert <commit-hash>`.
- Cách 2: Khôi phục bằng tay từ thư mục `backup_original/` bằng lệnh:
  `cp -r backup_original/* ./`

---

## 3. Hướng dẫn Cập nhật Nội dung Thủ công (Cho Admin)

Toàn bộ thông tin quan trọng giờ đây là **Data-driven**, nghĩa là bạn không cần đụng vào HTML/CSS.

### 3.1. Cập nhật Thành viên (People / Alumni)
1. Thêm mới 1 thành viên: Tạo một file `tên-không-dấu.md` trong thư mục `_people/`.
2. Định dạng file theo chuẩn Front-matter:
   ```yaml
   ---
   layout: person
   title: "Nguyễn Văn A"
   job_title: "Research Assistant"
   role_group: "Research Assistants" # Chọn: Executive Board, Research Assistants, Interns, Alumni
   order: 2
   department: "Khoa ABC"
   email: "abc@mail.com"
   photo: "/assets/images/people/anh.jpg"
   # ...các trường khác (linkedin, github, scholar)
   ---
   Mô tả chi tiết about me ở đây...
   ```
3. Thêm ảnh: Copy ảnh của thành viên vào thư mục `assets/images/people/`.

### 3.2. Cập nhật Báo cáo Khoa học (Publications)
Mở file `_data/publications.yml` và thêm vào đầu file theo cấu trúc sau:
```yaml
- title: "Tên bài báo"
  authors: "Tác giả 1, Tác giả 2"
  year: 2026
  type: "journal" # hoặc "conference"
  venue: "Tên Tạp chí/Hội nghị"
  thumbnail: "assets/images/publications/image.jpg"
  paper_link: "https://link-bài-báo"
  github_link: "https://link-code-nếu-có"
```

### 3.3. Cập nhật Tin tức & Hoạt động (News)
Mở file `_data/news.yml` và thêm vào danh sách:
```yaml
- title: "Tiêu đề tin tức"
  date: "2026-04-01"
  content: "Tóm tắt ngắn gọn nội dung tin tức..."
```
*(Số thứ tự tự động tính toán phân trang client-side mỗi trang 10 tin)*.

---

## 4. Manual QA & Accessibility Checklist (Tiếng Việt)

Khi bạn kiểm tra PR này hoặc build ở Local, vui lòng thực hiện các bước sau:
- [ ] **Home Page:** Hero section (hiển thị tỉ lệ 2:5), About Us font đẹp-dễ đọc, Gallery JS Slide chạy tốt (click mũi tên hoặc tự động chuyển hướng), Recent News phân trang hiển thị 10 bài/trang chạy Client-side.
- [ ] **Navigation:** Đảm bảo khi mở di động/thu nhỏ cửa sổ < 768px, menu Navbar hiện icon hamburger và click vào có hiệu ứng mở menu xổ dọc.
- [ ] **People Page:** Hiện rõ các Group members. Click vào mỗi card thành viên sẽ đưa tới trang profile đầy đủ.
- [ ] **Publications Page:** Dữ liệu được nhóm to theo Heading Năm (e.g. 2026, 2025). Hiển thị dưới dạng cột với ảnh bên trái và nội dung kèm Button bên phải. Button "View Paper" / "GitHub" hoạt động.
- [ ] **Gallery (Pics):** Click vào 1 ảnh, Lightbox (Modal hiển thị ảnh lớn) sẽ phóng to ra chính giữa màn hình (nền đen trong suốt). Nhấn `Esc` hoặc bấm `(X)` sẽ đóng mượt mà.
- [ ] **Accessibility (A11y):** Các hình ảnh đều có thẻ `alt` text. Hệ màu `xanh #339966 / nền sáng` đảm bảo tốt cho độ nhạy bén tương phản (Color contrast).
- [ ] **Broken Link:** Kiểm tra tab Datasets các links có bị lỗi hay dẫn vòng vo không.

---

Cảm ơn bạn! Mọi cấu trúc và module đã được tổ chức lại để website AgIL sẵn sàng nâng cấp hoặc thêm bao nhiêu dữ liệu tùy thích mà không lo lắng về việc lặp lại template (DRY Code).
