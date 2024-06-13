from .forms import MedidasForm


def carrito_counter(request):
    carrito = request.session.get("carrito", {})
    carrito_count = sum(carrito.values())
    return {"carrito_count": carrito_count}


def calcular_costo_adicional(request):
    costo_adicional_largo = 0
    costo_adicional_ancho = 0
    costo_adicional_alto = 0
    total_costo_adicional = 0

    if request.method == "POST":
        form = MedidasForm(request.POST)
        if form.is_valid():
            largo = form.cleaned_data["largo"]
            ancho = form.cleaned_data["ancho"]
            alto = form.cleaned_data["alto"]

            if largo >= 20:
                costo_adicional_largo = 35000
            elif largo >= 11 and largo <= 19:
                costo_adicional_largo = 25000
            elif largo >= 1 and largo <= 10:
                costo_adicional_largo = 15000

            if ancho >= 20:
                costo_adicional_ancho = 35000
            elif ancho >= 11 and ancho <= 19:
                costo_adicional_ancho = 25000
            elif ancho >= 1 and ancho <= 10:
                costo_adicional_ancho = 15000

            if alto >= 20:
                costo_adicional_alto = 35000
            elif alto >= 11 and alto <= 19:
                costo_adicional_alto = 25000
            elif alto >= 1 and alto <= 10:
                costo_adicional_alto = 15000

            total_costo_adicional = (
                costo_adicional_largo + costo_adicional_ancho + costo_adicional_alto
            )

    return {
        "costo_adicional_largo": costo_adicional_largo,
        "costo_adicional_ancho": costo_adicional_ancho,
        "costo_adicional_alto": costo_adicional_alto,
        "total_costo_adicional": total_costo_adicional,
    }
