document.addEventListener('DOMContentLoaded', function () {
    var verMasDetallesBtns = document.querySelectorAll('[data-bs-toggle="modal"]');
    var modalInfoCardContent = document.querySelector('.modal-info-card').innerHTML;

    verMasDetallesBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            var card = this.closest('.card');
            if (card) {
                var cardTitle = card.querySelector('.card-title').innerText;
                var cardBrand = card.querySelector('.card-brand').innerText;
                var cardStock = card.querySelector('.card-stock').innerText;
                var detalleProducto = document.getElementById('detalleProducto');

                detalleProducto.innerHTML = '<h5>' + cardTitle + '</h5><p>' + '</p><p>Clasificacion del Producto: ' + cardBrand + '</p><p>Stock disponible: ' + cardStock + '</p>' + modalInfoCardContent;
            }
        });
    });

    const form = document.querySelector('.search');
    const input = form.querySelector('input');
    const products = document.querySelectorAll('.card');

    input.addEventListener('input', function () {
        const searchTerm = input.value.trim().toLowerCase();

        products.forEach(function (product) {
            const title = product.querySelector('.card-title').textContent.toLowerCase();
            const brand = product.querySelector('.card-brand').textContent.toLowerCase();
            const type = product.querySelector('.Type-card').textContent.toLowerCase();

            if (title.includes(searchTerm) || brand.includes(searchTerm) || type.includes(searchTerm)) {
                product.style.transition = 'opacity 0.5s';
                product.style.opacity = '1';
                if (title.includes(searchTerm)) {
                    product.style.backgroundColor = '#ffcccc';
                } else {
                    product.style.backgroundColor = '';
                }
            } else {
                product.style.transition = 'opacity 0.5s';
                product.style.opacity = '0';
            }
        });
    });
});
