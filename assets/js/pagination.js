/* Tên file: pagination.js
* Mục đích: Hiệu ứng phân trang client-side cho trang Home (Recent News, 10 items/page)
* Test: Kiểm tra có hiện số trang, click chuyển trang.
*/

document.addEventListener('DOMContentLoaded', () => {
    const itemsPerPage = 10;
    const items = document.querySelectorAll('.agil-news-card');
    const paginationContainer = document.getElementById('news-pagination');

    if (items.length === 0 || !paginationContainer) return;

    const totalPages = Math.ceil(items.length / itemsPerPage);

    function showPage(page) {
        items.forEach((item, index) => {
            if (index >= (page - 1) * itemsPerPage && index < page * itemsPerPage) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });

        // Update active button
        const buttons = paginationContainer.querySelectorAll('button');
        buttons.forEach(btn => btn.style.backgroundColor = 'var(--agil-muted)');
        if (buttons[page - 1]) {
            buttons[page - 1].style.backgroundColor = 'var(--agil-primary-light)';
            buttons[page - 1].style.color = '#fff';
        }
    }

    // Create buttons
    if (totalPages > 1) {
        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement('button');
            btn.innerText = i;
            btn.style.padding = '5px 12px';
            btn.style.border = '1px solid var(--agil-border)';
            btn.style.borderRadius = 'var(--agil-radius)';
            btn.style.cursor = 'pointer';
            btn.style.backgroundColor = 'var(--agil-muted)';

            btn.addEventListener('click', () => {
                showPage(i);
            });
            paginationContainer.appendChild(btn);
        }
    }

    // Show first page initially
    showPage(1);
});
