from django import forms


class MedidasForm(forms.Form):
    largo = forms.IntegerField(label="Largo")
    ancho = forms.IntegerField(label="Ancho")
    alto = forms.IntegerField(label="Alto")
