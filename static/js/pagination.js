document.addEventListener("DOMContentLoaded", function () {
    const rowsPerPageSelect = document.getElementById("rowsPerPage");
    const table = document.getElementById("resultsTable");
    const paginationControls = document.getElementById("paginationControls");
    const rows = Array.from(table.querySelectorAll("tbody tr"));

    let rowsPerPage = parseInt(rowsPerPageSelect.value);
    let currentPage = 1;

    function renderTable() {
        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        rows.forEach((row, index) => {
            row.style.display = (index >= start && index < end) ? "" : "none";
        });

        renderPagination();
    }

    function renderPagination() {
        const pageCount = Math.ceil(rows.length / rowsPerPage);
        paginationControls.innerHTML = "";

        for (let i = 1; i <= pageCount; i++) {
            const btn = document.createElement("button");
            btn.textContent = i;
            if (i === currentPage) btn.style.backgroundColor = "#002d80";
            btn.addEventListener("click", () => {
                currentPage = i;
                renderTable();
            });
            paginationControls.appendChild(btn);
        }
    }

    rowsPerPageSelect.addEventListener("change", () => {
        rowsPerPage = parseInt(rowsPerPageSelect.value);
        currentPage = 1;
        renderTable();
    });

    renderTable();
});
