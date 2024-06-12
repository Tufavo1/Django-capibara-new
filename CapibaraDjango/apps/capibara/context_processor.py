def carrito_counter(request):
    carrito = request.session.get("carrito", {})
    carrito_count = sum(carrito.values())
    return {"carrito_count": carrito_count}
