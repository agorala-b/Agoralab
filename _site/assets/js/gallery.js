/* Tên file: gallery.js
 * Mục đích: Vanilla JS Lightbox hiệu ứng mở ảnh to khi nhấn vào ảnh
 * Test: Click vào một bức ảnh trong trang Pics
 */

document.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelectorAll('.agil-gallery-item img');
    const lightbox = document.getElementById('agil-lightbox');
    const lightboxImg = document.getElementById('agil-lightbox-img');
    const closeBtn = document.getElementById('agil-lightbox-close');

    if (!lightbox) return;

    items.forEach(item => {
        item.addEventListener('click', (e) => {
            lightboxImg.src = e.target.src;
            lightbox.style.display = 'flex';
        });
    });

    closeBtn.addEventListener('click', () => {
        lightbox.style.display = 'none';
        lightboxImg.src = '';
    });

    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            lightbox.style.display = 'none';
            lightboxImg.src = '';
        }
    });

    // Escape key handling
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && lightbox.style.display === 'flex') {
            lightbox.style.display = 'none';
            lightboxImg.src = '';
        }
    });
});
