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

    const form = document.getElementById("form-agregar-carrito");
    const mensajeExito = document.getElementById("mensaje-exito");
    const mensajeStock = document.getElementById("mensaje-stock");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (response.ok) {
                    mensajeExito.style.display = "block";
                    setTimeout(function () {
                        mensajeExito.style.display = "none";
                    }, 3000);
                } else if (response.status === 400) {
                    response.json()
                        .then(data => {
                            if (data.error === "invalid_quantity") {
                                console.error('Error en el servidor:', data.error);
                            } else if (data.error === "out_of_stock") {
                                mensajeStock.style.display = "block";
                                setTimeout(function () {
                                    mensajeStock.style.display = "none";
                                }, 3000);
                            } else {
                                console.error('Error en el servidor:', data.error);
                            }
                        });
                } else {
                    console.error('Error en la solicitud fetch:', response.statusText);
                }
            })
            .catch(error => console.error('Error en la solicitud fetch:', error));
    });

    const checkboxes = document.querySelectorAll('.categoria-checkbox');
    const productos = document.querySelectorAll('.abrir-producto');

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            const categoriasSeleccionadas = obtenerCategoriasSeleccionadas();
            filtrarProductosPorCategoria(categoriasSeleccionadas);
        });
    });

    function obtenerCategoriasSeleccionadas() {
        const categoriasSeleccionadas = [];
        checkboxes.forEach(function (checkbox) {
            if (checkbox.checked) {
                categoriasSeleccionadas.push(parseInt(checkbox.value));
            }
        });
        return categoriasSeleccionadas;
    }

    function filtrarProductosPorCategoria(categoriasSeleccionadas) {
        productos.forEach(function (producto) {
            const categoriaProducto = parseInt(producto.getAttribute('data-categoria'));
            if (categoriasSeleccionadas.length === 0 || categoriasSeleccionadas.includes(categoriaProducto)) {
                producto.style.display = 'block';
            } else {
                producto.style.display = 'none';
            }
        });
    }
});
