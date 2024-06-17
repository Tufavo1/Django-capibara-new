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
});
