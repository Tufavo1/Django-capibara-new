document.addEventListener('DOMContentLoaded', function () {
    var btnClasificacion = document.getElementById('btn-clasificacion');
    var divClasificacion = document.getElementById('clasificacion');
    var btnClose = document.getElementById('btn-close');
    var btnCalcular = document.getElementById('btn-calcular');
    var medidasForm = document.getElementById('medidas-form');
    var costoAdicionalSpan = document.getElementById('costo-adicional');
    var costoAdicionalLista = document.getElementById('costo-adicional-lista');
    var inputCostoAdicional = document.getElementById('input-costo-adicional');
    var btnAddToCart = document.getElementById('btn-add-to-cart');

    btnClasificacion.addEventListener('click', function () {
        divClasificacion.style.display = 'block';
        btnClasificacion.style.display = 'none';
    });

    btnClose.addEventListener('click', function () {
        divClasificacion.style.display = 'none';
        btnClasificacion.style.display = 'block';
    });

    btnCalcular.addEventListener('click', function () {
        var largo = parseInt(document.getElementById('largo').value) || 0;
        var ancho = parseInt(document.getElementById('ancho').value) || 0;
        var alto = parseInt(document.getElementById('alto').value) || 0;

        var costoLargo = calcularCosto(largo);
        var costoAncho = calcularCosto(ancho);
        var costoAlto = calcularCosto(alto);

        var costoTotal = costoLargo + costoAncho + costoAlto;

        document.getElementById('costo-adicional-valor').textContent = costoTotal.toLocaleString();
    });

    medidasForm.addEventListener('submit', function (event) {
        event.preventDefault();

        var largo = parseInt(document.getElementById('largo').value) || 0;
        var ancho = parseInt(document.getElementById('ancho').value) || 0;
        var alto = parseInt(document.getElementById('alto').value) || 0;

        var costoLargo = calcularCosto(largo);
        var costoAncho = calcularCosto(ancho);
        var costoAlto = calcularCosto(alto);

        var costoTotal = costoLargo + costoAncho + costoAlto;

        if (costoAdicionalSpan) {
            costoAdicionalSpan.textContent = costoTotal.toLocaleString();
        }

        if (costoAdicionalLista) {
            costoAdicionalLista.style.display = 'block';
        }

        inputCostoAdicional.value = costoTotal;

        divClasificacion.style.display = 'none';
        btnClasificacion.style.display = 'block';
    });

    function calcularCosto(valor) {
        if (valor >= 20) {
            return 35000;
        } else if (valor >= 11 && valor <= 19) {
            return 25000;
        } else if (valor >= 1 && valor <= 10) {
            return 15000;
        } else {
            return 0;
        }
    }

    btnAddToCart.addEventListener('click', function () {
        var costoAdicional = parseInt(document.getElementById('costo-adicional-valor').textContent.replace(/,/g, '')) || 0;
        inputCostoAdicional.value = costoAdicional;
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

});

$(document).ready(function () {
    $("#confirmar-envio").click(function () {
        var zonaSeleccionada = $("#zona").val();

        if (zonaSeleccionada === "") {
            alert("Seleccione una zona antes de confirmar el envío.");
            return;
        }

        var codigosProductos = [];
        $(".producto-cod").each(function () {
            codigosProductos.push($(this).text());
        });

        $.ajax({
            url: "/calcular_despacho/",
            type: "POST",
            data: {
                zona: zonaSeleccionada,
                codigos_productos: codigosProductos
            },
            success: function (response) {
                $("#Cost-despacho").text(response.costo_despacho);
            },
            error: function (xhr, status, error) {
                console.error("Error al calcular el costo de despacho:", error);
            }
        });
    });
});