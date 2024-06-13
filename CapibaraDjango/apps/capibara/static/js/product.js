document.addEventListener('DOMContentLoaded', function () {
    var btnClasificacion = document.getElementById('btn-clasificacion');
    var divClasificacion = document.getElementById('clasificacion');
    var btnClose = document.getElementById('btn-close');

    // Mostrar formulario al hacer clic en "Personalizar Producto"
    btnClasificacion.addEventListener('click', function () {
        divClasificacion.style.display = 'block';
        btnClasificacion.style.display = 'none';
    });

    btnClose.addEventListener('click', function () {
        divClasificacion.style.display = 'none';
        btnClasificacion.style.display = 'block';
    });
});