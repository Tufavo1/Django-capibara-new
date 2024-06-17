from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User


class EditUserForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ("email", "password", "confirm_password", "direccion")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
