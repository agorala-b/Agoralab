document.addEventListener('DOMContentLoaded', () => {
    // Select the search button from the navigation
    const searchBtn = document.getElementById('search-btn');

    // Add a click event listener
    searchBtn.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent default link behavior
        
        // Placeholder for future search functionality
        alert('Search functionality would be triggered here.');
    });
});