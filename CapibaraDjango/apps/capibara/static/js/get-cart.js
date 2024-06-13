document.addEventListener('DOMContentLoaded', function () {
    var shippingForm = document.getElementById("shipping-form");
    var shippingDetailsSection = document.getElementById("shipping-details");
    var editarDireccionButton = document.getElementById("editar-direccion");

    shippingForm.addEventListener("change", function (event) {
        if (event.target.value === "domicilio") {
            shippingDetailsSection.style.display = "block";
            disableFormFields(shippingDetailsSection);
            editarDireccionButton.style.display = "block";

        } else if (event.target.value === "retiro") {
            shippingDetailsSection.style.display = "none";
            pickupDetailsSection.style.display = "block";
            editarDireccionButton.style.display = "none";
        }
    });

    var confirmarEnvioButton = document.getElementById("confirmar-envio");

    confirmarEnvioButton.addEventListener("click", function () {
        var costoEnvio = calcularCostoEnvio(document.getElementById("zona").value);
        var subtotalActual = parseFloat(document.getElementById("Sub-cart").textContent.substring(1));
        var nuevoTotal = subtotalActual + costoEnvio;

        document.getElementById("Cost-despacho").textContent = "$" + costoEnvio.toFixed(0);
        document.getElementById("Total-cart").textContent = "$" + nuevoTotal.toFixed(0);

        alert("Detalles de envío confirmados");
        disableFormFields(shippingDetailsSection);
        editarDireccionButton.style.display = "block";
    });

    editarDireccionButton.addEventListener("click", function () {
        enableFormFields(shippingDetailsSection);
        editarDireccionButton.style.display = "none";
    });

    function disableFormFields(form) {
        var fields = form.querySelectorAll("input, select, textarea");
        for (var i = 0; i < fields.length; i++) {
            fields[i].disabled = true;
        }
    }

    function enableFormFields(form) {
        var fields = form.querySelectorAll("input, select, textarea");
        for (var i = 0; i < fields.length; i++) {
            fields[i].disabled = false;
        }
    }

    function calcularCostoEnvio(zona) {
        var preciosPorZona = {
            "Zona 1 (Arica y Parinacota - Antofagasta)": {
                1001: 30000,
                1002: 60000,
                1003: 15000,
                1004: 60000,
                1005: 120000,
                1006: 120000,
                1007: 20000,
                1008: 30000
            },
            "Zona 2 (Atacama - Coquimbo)": {
                1001: 30000,
                1002: 60000,
                1003: 15000,
                1004: 60000,
                1005: 120000,
                1006: 120000,
                1007: 20000,
                1008: 30000
            },
            "Zona 3 (Valparaiso - Maule)": {
                1001: 30000,
                1002: 15000,
                1003: 10000,
                1004: 30000,
                1005: 100000,
                1006: 100000,
                1007: 20000,
                1008: 30000
            },
            "Zona 4 (BIOBIO - Los Lagos)": {
                1001: 50000,
                1002: 60000,
                1003: 10000,
                1004: 30000,
                1005: 100000,
                1006: 100000,
                1007: 20000,
                1008: 30000
            },
            "Zona 5 (Aysen - Magallanes)": {
                1001: 50000,
                1002: 60000,
                1003: 15000,
                1004: 60000,
                1005: 120000,
                1006: 120000,
                1007: 20000,
                1008: 30000
            }
        };

        var cart = JSON.parse(localStorage.getItem("carritoCompras")) || [];
        var costoTotalEnvio = 0;

        cart.forEach(function (product) {
            if (preciosPorZona[zona] && preciosPorZona[zona][product.id]) {
                costoTotalEnvio += preciosPorZona[zona][product.id];
            }
        });

        return costoTotalEnvio;
    }
});