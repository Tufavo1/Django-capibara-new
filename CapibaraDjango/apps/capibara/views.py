from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MedidasForm


# Create your views here.
def CargarHome(request):
    productos = Producto.objects.filter(stock__gt="0").order_by("nombre")
    categorias = Categoria.objects.all()
    muebles = Mueble.objects.values("nombre").distinct()

    productos_destacados_por_categoria = []
    for categoria in categorias:
        productos_destacados = Producto.objects.filter(
            categoria=categoria,
            stock__gt=0,
            ventas__gt=0,
        ).order_by("-ventas")[:1]
        productos_destacados_por_categoria.append((categoria, productos_destacados))

    return render(
        request,
        "pages/home.html",
        {
            "productos": productos,
            "cate": categorias,
            "mueble": muebles,
            "productos_destacados_por_categoria": productos_destacados_por_categoria,
        },
    )


def ver_producto(request, p_cod):
    producto = get_object_or_404(Producto, cod=p_cod)
    costo_adicional = 0

    if request.method == "POST":
        form = MedidasForm(request.POST)
        if form.is_valid():
            largo = form.cleaned_data["largo"]
            ancho = form.cleaned_data["ancho"]
            alto = form.cleaned_data["alto"]

            if largo >= 20:
                costo_adicional += 35000
            elif largo >= 11 and largo <= 19:
                costo_adicional += 25000
            elif largo >= 1 and largo <= 10:
                costo_adicional += 15000

            if ancho >= 20:
                costo_adicional += 35000
            elif ancho >= 11 and ancho <= 19:
                costo_adicional += 25000
            elif ancho >= 1 and ancho <= 10:
                costo_adicional += 15000

            if alto >= 20:
                costo_adicional += 35000
            elif alto >= 11 and alto <= 19:
                costo_adicional += 25000
            elif alto >= 1 and alto <= 10:
                costo_adicional += 15000

    else:
        form = MedidasForm()

    context = {
        "producto": producto,
        "form": form,
        "costo_adicional": costo_adicional,
    }
    return render(request, "pages/view_product.html", context)


def CargarProductos(request):
    productos = Producto.objects.filter(stock__gt="0").order_by("nombre")
    muebles = Mueble.objects.all()
    categorias = Producto.objects.values("categoria").distinct()
    paginator = Paginator(productos, 9)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/productos.html",
        {
            "prod": page_products,
            "cate": categorias,
            "mueb": muebles,
        },
    )


def CargarCocina(request):
    prodCoci = Producto.objects.filter(stock__gt="0", categoria="1").order_by("nombre")
    muebles = Mueble.objects.all()
    categorias = Producto.objects.values("categoria").distinct()
    paginator = Paginator(prodCoci, 6)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/comedor.html",
        {"prod": page_products, "mueb": muebles, "cat": categorias},
    )


def CargarComedor(request):
    prodCom = Producto.objects.filter(stock__gt="0", categoria="3").order_by("nombre")
    muebles = Mueble.objects.all()
    categorias = Producto.objects.values("categoria").distinct()
    paginator = Paginator(prodCom, 6)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/comedor.html",
        {"prod": page_products, "mueb": muebles, "cat": categorias},
    )


def CargarDormitorio(request):
    prodDorm = Producto.objects.filter(stock__gt="0", categoria="2").order_by("nombre")
    muebles = Mueble.objects.all()
    categorias = Producto.objects.values("categoria").distinct()
    paginator = Paginator(prodDorm, 6)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/comedor.html",
        {"prod": page_products, "mueb": muebles, "cat": categorias},
    )


@login_required
def agregar_opinion(request, p_cod):
    if request.method == "POST":
        username = request.user.username
        calificacion = request.POST.get("calificacion")
        comentario = request.POST.get("comentario")

        productos = Producto.objects.get(cod=p_cod)

        opinion = Opinion.objects.create(
            producto=productos,
            username=username,
            calificacion=calificacion,
            comentario=comentario,
        )

        opinion.save()

        return redirect("ver_producto", cod=p_cod)
    else:
        return redirect("home")


def CargarContacto(request):
    return render(request, "pages/contacto.html")


@require_POST
def agregar_al_carrito(request):
    producto_cod = request.POST.get("producto_cod")
    cantidad = 1
    producto = get_object_or_404(Producto, cod=producto_cod)

    if cantidad > 0 and cantidad <= producto.stock:
        carrito = request.session.get("carrito", {})
        if producto_cod in carrito:
            if carrito[producto_cod] + cantidad <= producto.stock:
                carrito[producto_cod] += cantidad
            else:
                return redirect("ver_producto", p_cod=producto_cod)
        else:
            carrito[producto_cod] = cantidad

        request.session["carrito"] = carrito
        request.session.modified = True
    else:
        return redirect("ver_producto", p_cod=producto_cod)

    return redirect("ver_producto", p_cod=producto_cod)


def CargarCarrito(request):
    carrito = request.session.get("carrito", {})
    productos = Producto.objects.filter(cod__in=carrito.keys())

    # Crear una lista de diccionarios con cada producto y su cantidad en el carrito
    carrito_items = [
        {"producto": producto, "cantidad": carrito[str(producto.cod)]}
        for producto in productos
    ]

    context = {"carrito_items": carrito_items}
    return render(request, "pages/carrito.html", context)


def acceso(request):
    context = {}

    if request.method == "POST":
        if "User" in request.POST and "loginPassword" in request.POST:
            # Login logic
            usuario = request.POST.get("User")
            clave = request.POST.get("loginPassword")
            user = authenticate(request, username=usuario, password=clave)
            if user is not None:
                login(request, user)
                return redirect("/home")
            else:
                print("Credenciales inválidas")
                context["error"] = "Credenciales inválidas. Intente nuevamente."
        elif (
            "registerNombre" in request.POST
            and "registerEmail" in request.POST
            and "registerPassword" in request.POST
            and "registerNombreCompleto" in request.POST
            and "registerTelefono" in request.POST
            and "registerDireccion" in request.POST
        ):
            # Register logic
            nombre_usuario = request.POST.get("registerNombre")
            correo = request.POST.get("registerEmail")
            contraseña = request.POST.get("registerPassword")
            nombre_real = request.POST.get("registerNombreCompleto")
            telefono = request.POST.get("registerTelefono")
            direccion = request.POST.get("registerDireccion")

            user = User.objects.create_user(
                username=nombre_usuario,
                email=correo,
                password=contraseña,
                nombre=nombre_real,
                telefono=telefono,
                direccion=direccion,
            )
            user.save()

            login(request, user)
            return redirect("/home")

    return render(request, "pages/acceso.html", context)


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/home")
