document.addEventListener("DOMContentLoaded", function () {
    var usuarioIniciado = JSON.parse(localStorage.getItem("UsuarioIniciado"));

    if (usuarioIniciado) {
        document.getElementById("fullName").innerText = usuarioIniciado.nombre;
        document.getElementById("birthdate").innerText = usuarioIniciado.fechaNacimiento;
        document.getElementById("email").innerText = usuarioIniciado.email;

        var passwordField = document.getElementById("password");
        if (!passwordField) {
            var passwordContainer = document.querySelector("#passwordRow .col-sm-8");
            passwordField = document.createElement("span");
            passwordField.id = "password";
            passwordContainer.appendChild(passwordField);
        }
        passwordField.innerText = "*".repeat(usuarioIniciado.password.length);
    }

    var editBtn = document.getElementById("editBtn");
    var cancelBtn = document.getElementById("cancelBtn");
    var saveBtn = document.getElementById("saveBtn");
    var newPasswordField = document.getElementById("newPassword");
    var confirmNewPasswordField = document.getElementById("confirmNewPassword");

    editBtn.addEventListener("click", function () {
        if (editBtn.innerText === "Editar Información") {
            editBtn.style.display = "none";
            cancelBtn.style.display = "inline-block";
            saveBtn.style.display = "inline-block";
            document.getElementById("passwordRow").style.display = "block";
            document.getElementById("password").style.display = "none";
            newPasswordField.style.display = "block";
            confirmNewPasswordField.style.display = "block";
        }
    });

    cancelBtn.addEventListener("click", function () {
        editBtn.style.display = "inline-block";
        cancelBtn.style.display = "none";
        saveBtn.style.display = "none";
        newPasswordField.style.display = "none";
        confirmNewPasswordField.style.display = "none";
    });

    saveBtn.addEventListener("click", function () {
        var newPassword = newPasswordField.value;
        var confirmNewPassword = confirmNewPasswordField.value;

        if (newPassword !== confirmNewPassword) {
            alert("Las contraseñas no coinciden");
            return;
        }

        usuarioIniciado.email = document.getElementById("email").innerText;
        if (newPassword) {
            usuarioIniciado.password = newPassword;
        }

        localStorage.setItem("UsuarioIniciado", JSON.stringify(usuarioIniciado));
        alert("Información actualizada correctamente");

        editBtn.style.display = "inline-block";
        cancelBtn.style.display = "none";
        saveBtn.style.display = "none";
        newPasswordField.style.display = "none";
        confirmNewPasswordField.style.display = "none";
    });
});
