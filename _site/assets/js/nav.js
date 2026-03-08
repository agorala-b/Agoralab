/* Tên file: nav.js
 * Mục đích: Hiển thị/ẩn menu responsive trên mobile (hamburger menu)
 * Cách test: Thu nhỏ màn hình trình duyệt < 768px, click vào hamburger icon để xem menu xổ xuống.
 * Rollback: git checkout HEAD -- assets/js/nav.js
 */

document.addEventListener('DOMContentLoaded', () => {
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.getElementById('nav-links');

    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileBtn.classList.toggle('active');
        });
    }
});
