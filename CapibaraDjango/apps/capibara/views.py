<<<<<<< HEAD
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
=======
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
>>>>>>> 6d601b0219bff7d91a85639ee03efb7955e4df6a


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
    return render(request, "pages/view_product.html", {"producto": producto})


def CargarProductos(request):
    categoria_id = request.GET.get("categoria_id")
    muebles = Mueble.objects.all()
    categoria = Categoria.objects.all()

    if categoria_id:
        productos = Producto.objects.filter(
            stock__gt=0, tipomueble=categoria_id
        ).order_by("nombre")
    else:
        productos = Producto.objects.filter(stock__gt=0).order_by("nombre")

    paginator = Paginator(productos, 8)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos.html",
        {"productos": page_products, "cate": categoria, "mueble": muebles},
    )


def CargarCocina(request):
    prodCocina = Producto.objects.filter(stock__gt="0", categoria_id="1").order_by(
        "nombre"
    )
    categorias = Categoria.objects.all()
    muebles = Mueble.objects.values("nombre").distinct()
    paginator = Paginator(prodCocina, 6)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/cocina.html",
        {"productos": page_products, "cate": categorias, "mueble": muebles},
    )


def CargarComedor(request):
    prodComedor = Producto.objects.filter(stock__gt="0", categoria_id="3").order_by(
        "nombre"
    )
    categorias = Categoria.objects.all()
    muebles = Mueble.objects.values("nombre").distinct()
    paginator = Paginator(prodComedor, 6)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/comedor.html",
        {"productos": page_products, "cate": categorias, "mueble": muebles},
    )


def CargarDormitorio(request):
    productos = Producto.objects.filter(stock__gt="0", categoria_id="2").order_by(
        "nombre"
    )
    categorias = Categoria.objects.all()
    muebles = Mueble.objects.values("nombre").distinct()
    paginator = Paginator(productos, 6)
    page_number = request.GET.get("page")
    page_products = paginator.get_page(page_number)

    return render(
        request,
        "pages/productos/dormitorio.html",
        {"productos": page_products, "cate": categorias, "mueble": muebles},
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


<<<<<<< HEAD
@require_POST
def agregar_al_carrito(request):
    producto_cod = request.POST.get("producto_cod")
    carrito = request.session.get("carrito", {})

    if producto_cod in carrito:
        carrito[producto_cod] += 1
    else:
        carrito[producto_cod] = 1

    request.session["carrito"] = carrito
    request.session.modified = True
    return redirect("ver_producto", p_cod=producto_cod)


def CargarCarrito(request):
    carrito = request.session.get("carrito", {})
    productos = Producto.objects.filter(cod__in=carrito.keys())
    carrito_items = [
        {"producto": producto, "cantidad": carrito[str(producto.cod)]}
        for producto in productos
    ]
    context = {"carrito_items": carrito_items}
    return render(request, "pages/carrito.html", context)
=======

#login
def acceso(request):
    context = {}  # Define el contexto vacío al principio.

    if request.method == 'POST':
        if 'User' in request.POST and 'loginPassword' in request.POST:
            usuario = request.POST.get('User')
            clave = request.POST.get('loginPassword')
            user = authenticate(request, username=usuario, password=clave)
            if user is not None:

                login(request, user)
                return redirect('/home')
            else:
                print("Credenciales inválidas")  # Depuración
                context['error'] = 'Credenciales inválidas. Intente nuevamente.'

        elif 'registerNombre' in request.POST and 'registerEmail' in request.POST and 'registerPassword' in request.POST:
            nombre_usuario = request.POST.get('registerNombre')
            correo = request.POST.get('registerEmail')
            contraseña = request.POST.get('registerPassword')

            # Crea un nuevo usuario
            user = User.objects.create_user(username=nombre_usuario, email=correo, password=contraseña)
            login(request, user)
            
            # Usuario registrado con éxito, puedes redirigirlo al inicio u otra página.
            return redirect('/home')
    #Renderiza la plantilla con el contexto, ya sea que el usuario se autentique o no.
    return render(request, 'pages/acceso.html', context)

def logout_view(request):
    if request.method == 'POST':
        # Si se envía una solicitud POST con el nombre 'logout', entonces realiza el logout.
        logout(request)
        return redirect('/home')   
>>>>>>> 6d601b0219bff7d91a85639ee03efb7955e4df6a
