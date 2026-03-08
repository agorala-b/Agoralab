# Hướng dẫn Chạy và Quản lý Website — AgIL

Website AgIL được xây dựng bằng HTML tĩnh, CSS và JavaScript thuần. Do cơ chế bảo mật của trình duyệt (CORS), bạn cần chạy qua web server local khi phát triển.

## 1. Cách chạy Local Server

```bash
cd /home/viet/Downloads/web
python3 -m http.server 8080
```

Mở trình duyệt: [http://localhost:8080/](http://localhost:8080/)

---

## 2. Các trang chính

| Trang | File | Mô tả |
|-------|------|--------|
| **Trang chủ** | `index.html` | About Us, carousel, news |
| **Research** | `research.html` | Hướng nghiên cứu của lab |
| **Members** | `member.html` | Danh sách thành viên |
| **Profile** | `member/profile.html?m=ten_member` | Profile cá nhân (dùng chung) |
| **Publications** | `publications.html` | Bài báo khoa học |
| **Datasets** | `datasets.html` | Dữ liệu mở |
| **Activities** | `activities.html` | Sự kiện, hoạt động |

---

## 3. Cấu trúc thư mục

```
web/
├── index.html              # Trang chủ (entry point)
├── member.html             # Danh sách thành viên
├── publications.html       # Danh sách bài báo
├── research.html           # Nghiên cứu
├── activities.html         # Hoạt động
├── datasets.html           # Datasets
├── publications.bib        # File BibTeX nguồn (export từ Google Scholar)
├── assets/
│   ├── css/main.css        # CSS chung (palette xanh lá, font Calibri)
│   ├── css/style-guide.md  # Tài liệu design system
│   ├── js/main.js          # JS chung (carousel, menu)
│   └── images/carousel/    # Ảnh carousel và Logo (slide_1.png)
├── member/
│   ├── profile.html        # Template profile dùng chung
│   ├── default_avatar.svg  # Avatar mặc định
│   ├── <ten_member>/       # Folder riêng mỗi thành viên
│   │   ├── <ten>.yml       # Dữ liệu YAML
│   │   └── <ten>.jpg       # Ảnh đại diện
├── publications/
│   ├── data/publications.yml # Metadata bài báo (Auto-generated)
│   └── images/             # Thumbnail bài báo
├── scripts/
│   └── bib2yaml.py         # Script convert BibTeX -> YAML
└── tests/
    └── check_links.py      # Script kiểm tra links
```

---

## 4. Thêm Thành viên mới

1. Tạo folder: `member/nguyen_van_a/`
2. Thêm file YAML: `nguyen_van_a.yml` (copy từ template `member/member.yml`)
3. Thêm ảnh: `nguyen_van_a.jpg` vào cùng folder
4. Thêm `<div class="member-card">` vào `member.html` ở đúng section

---

## 5. Cập nhật Publication (Tự động)

Website sử dụng pipeline: **Google Scholar → BibTeX → YAML**.

1. **Lấy dữ liệu**: Export BibTeX từ Google Scholar các bài báo mới.
2. **Cập nhật nguồn**: Mở file `publications.bib` ở thư mục gốc, paste nội dung BibTeX vào cuối file.
3. **Chạy Script chuyển đổi**:
   ```bash
   python3 scripts/bib2yaml.py
   ```
4. **Kiểm tra**: Script sẽ tự động lọc bài trùng (duplicate), sắp xếp theo năm giảm dần và tạo file `publications/data/publications.yml`.
5. **Thumbnail**: Nếu muốn thêm ảnh minh họa bài báo, copy ảnh vào `publications/images/` và đặt tên trùng với field `thumbnail` trong YAML (mặc định là `example_pub.png`).

---

## 6. Chạy Tests

```bash
# Kiểm tra links trong YAML
python3 tests/check_links.py
```

---

## 7. Design System

Xem chi tiết tại: `assets/css/style-guide.md`

- **Màu chính**: `#339966` (xanh lá AgIL)
- **Logo**: Sử dụng file `assets/images/carousel/slide_1.png` trên Navbar.
- **Font**: Calibri, Arial, sans-serif (Font chuẩn hóa cho lab)
- **Spacing**: 8px grid system
- **CSS**: Tất cả styles tập trung trong `assets/css/main.css`

---

## 8. Rollback

Nếu cần khôi phục giao diện cũ:

```bash
git revert <hash>
```

Hoặc khôi phục các file CSS cũ (`des.css`, `mem.css`, `style.css`) và đổi link trong HTML.
