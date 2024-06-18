document.addEventListener('DOMContentLoaded', function () {
    const formsearch = document.querySelector('.search');
    const input = formsearch.querySelector('input');
    const products = document.querySelectorAll('.abrir-producto');

    input.addEventListener('input', function () {
        const searchTerm = input.value.trim().toLowerCase();

        products.forEach(function (product) {
            const title = product.querySelector('.card-title').textContent.toLowerCase();
            const price = product.querySelector('.price').textContent.toLowerCase();
            const stock = product.querySelector('.stock').textContent.toLowerCase();

            if (title.includes(searchTerm) || price.includes(searchTerm) || stock.includes(searchTerm)) {
                product.style.display = 'block';
            } else {
                product.style.display = 'none';
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
                product.style.display = 'block';
            } else {
                product.style.display = 'none';
            }
        });
    });

    document.querySelectorAll('form#form-agregar-carrito').forEach(function (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            const mensajeExito = form.querySelector("#mensaje-exito");
            const mensajeStock = form.querySelector("#mensaje-stock");

            const formData = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        mensajeExito.style.display = "block";
                        setTimeout(function () {
                            mensajeExito.style.display = "none";
                        }, 3000);
                    } else if (data.error === "invalid_quantity") {
                        console.error('Error en el servidor:', data.error);
                    } else if (data.error === "out_of_stock") {
                        mensajeStock.style.display = "block";
                        setTimeout(function () {
                            mensajeStock.style.display = "none";
                        }, 3000);
                    } else {
                        console.error('Error en el servidor:', data.error);
                    }
                })
                .catch(error => console.error('Error en la solicitud fetch:', error));
        });
    });

    // Filter by Category (Checkbox Changes)
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const selectedCategoryIds = Array.from(checkboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.value);

            products.forEach(product => {
                const productCategoryIds = product.dataset.categoria.split(',');
                const showProduct = selectedCategoryIds.length === 0 ||
                    productCategoryIds.some(id => selectedCategoryIds.includes(id));

                product.style.display = showProduct ? 'block' : 'none';
            });
        });
    });
});
