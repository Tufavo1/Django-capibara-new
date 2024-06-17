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
});
