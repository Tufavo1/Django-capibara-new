document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.search');
    const input = form.querySelector('input');
    const products = document.querySelectorAll('.abrir-producto');

    input.addEventListener('input', function () {
        const searchTerm = input.value.trim().toLowerCase();

        products.forEach(function (product) {
            const title = product.querySelector('.card-title').textContent.toLowerCase();
            const price = product.querySelector('.price').textContent.toLowerCase();
            const stock = product.querySelector('.stock').textContent.toLowerCase();

            if (title.includes(searchTerm) || price.includes(searchTerm) || stock.includes(searchTerm)) {
                product.style.display = 'block'; // Mostrar producto si coincide con el término de búsqueda
            } else {
                product.style.display = 'none'; // Ocultar producto si no coincide
            }
        });
    });

    const filterButton = document.getElementById('filter-prod');
    filterButton.addEventListener('click', function () {
        const minPrice = parseFloat(document.getElementById('minPrice').value) || 0;
        const maxPrice = parseFloat(document.getElementById('maxPrice').value) || Infinity;
        const selectedCategories = document.querySelectorAll('input[name="categoria"]:checked');

        products.forEach(function (product) {
            const productPrice = parseFloat(product.getAttribute('data-precio'));
            const productCategory = product.getAttribute('data-categoria').toLowerCase();

            const priceInRange = productPrice >= minPrice && productPrice <= maxPrice;
            const categoryMatch = Array.from(selectedCategories).some(function (category) {
                return productCategory.includes(category.value);
            });

            if (priceInRange && (selectedCategories.length === 0 || categoryMatch)) {
                product.style.display = 'block'; // Mostrar producto si cumple con los filtros de precio y categoría
            } else {
                product.style.display = 'none'; // Ocultar producto si no cumple con los filtros
            }
        });
    });
});
