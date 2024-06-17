$(document).ready(function () {
    const loginText = $(".title-text .login");
    const loginForm = $("form.login");
    const loginBtn = $("label.login");
    const signupBtn = $("label.signup");
    const signupLink = $("form .signup-link a");

    signupBtn.click(() => {
        loginForm.css("margin-left", "-50%");
        loginText.css("margin-left", "-50%");
    });

    loginBtn.click(() => {
        loginForm.css("margin-left", "0%");
        loginText.css("margin-left", "0%");
    });

    signupLink.click(() => {
        signupBtn.click();
        return false;
    });

    $('.btn-sidebar').click(function () {
        var target = $(this).data('target');
        $('.section').hide();
        $('main').show();
        $('.' + target).show();
    });

    const generateButton = document.getElementById('generateUsernameButton');
    const usernameField = document.getElementById('registerUsername');

    generateButton.addEventListener('click', function () {
        fetch('/generate-username/')
            .then(response => response.json())
            .then(data => {
                usernameField.value = data.username;
            })
            .catch(error => console.error('Error:', error));
    });
});

function togglePasswordVisibility() {
    const passwordField = document.getElementById('registerPassword');
    const iconEye = document.getElementById('icon-eye');
    const iconEyeSlash = document.getElementById('icon-eye-slash');

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        iconEye.style.display = 'none';
        iconEyeSlash.style.display = 'inline';
    } else {
        passwordField.type = 'password';
        iconEye.style.display = 'inline';
        iconEyeSlash.style.display = 'none';
    }
}
