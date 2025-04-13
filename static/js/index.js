document.addEventListener('DOMContentLoaded', function () {
    const table = document.getElementById('resultsTable');
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    const rowCountSelect = document.getElementById('rowCount');
    const pagination = document.getElementById('pagination');

    function paginateTable(perPage) {
        let currentPage = 1;

        function renderPage() {
            const start = (currentPage - 1) * perPage;
            const end = start + perPage;

            rows.forEach((row, index) => {
                row.style.display = index >= start && index < end ? '' : 'none';
            });

            renderPagination();
        }

        function renderPagination() {
            pagination.innerHTML = '';
            const totalPages = Math.ceil(rows.length / perPage);

            for (let i = 1; i <= totalPages; i++) {
                const btn = document.createElement('button');
                btn.innerText = i;
                btn.className = i === currentPage ? 'active-page' : '';
                btn.onclick = () => {
                    currentPage = i;
                    renderPage();
                };
                pagination.appendChild(btn);
            }
        }

        renderPage();
    }

    rowCountSelect.addEventListener('change', function () {
        paginateTable(parseInt(this.value));
    });

    paginateTable(parseInt(rowCountSelect.value));
});
