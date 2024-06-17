from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
import string
import random
from django.db import IntegrityError
from .mercadopago import *


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

    context = {"producto": producto}
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
                return JsonResponse({"error": "out_of_stock"}, status=400)
        else:
            carrito[producto_cod] = cantidad

        request.session["carrito"] = carrito
        request.session.modified = True
    else:
        return JsonResponse({"error": "invalid_quantity"}, status=400)

    return JsonResponse({"success": "Producto agregado al carrito."})


def CargarCarrito(request):
    carrito = request.session.get("carrito", {})
    codigos_productos = list(carrito.keys())
    productos = Producto.objects.filter(cod__in=codigos_productos)

    carrito_items = []
    for producto in productos:
        cantidad = carrito[str(producto.cod)]
        carrito_items.append({"producto": producto, "cantidad": cantidad})

    context = {"carrito_items": carrito_items}
    return render(request, "pages/carrito.html", context)


def eliminar_producto(request, cod_producto):
    if request.method == "POST":
        carrito = request.session.get("carrito", {})
        if str(cod_producto) in carrito:
            del carrito[str(cod_producto)]
            request.session["carrito"] = carrito
        return redirect("carrito")

    return HttpResponse(status=405)


def vaciar_carrito(request):
    if request.method == "POST":
        request.session["carrito"] = {}
        return redirect("carrito")

    return HttpResponse(status=405)


@login_required
def perfil(request):
    context = {}
    user = request.user

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        direccion = request.POST.get("direccion")
        new_password = request.POST.get("newPassword")
        confirm_new_password = request.POST.get("confirmNewPassword")

        if not email:
            messages.error(request, "El email no puede estar vacío.")
            context["error"] = "El email no puede estar vacío."
        elif new_password and new_password != confirm_new_password:
            messages.error(request, "Las contraseñas no coinciden.")
            context["error"] = "Las contraseñas no coinciden."
        else:
            user.nombre = nombre
            user.email = email
            user.direccion = direccion

            if new_password:
                user.set_password(new_password)

            try:
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Perfil actualizado exitosamente.")
                return redirect("perfil")
            except Exception as e:
                messages.error(request, f"Error al actualizar el perfil: {e}")
                context["error"] = f"Error al actualizar el perfil: {e}"

    boletas = Boleta.objects.filter(comprador=user)
    context["boletas"] = boletas
    return render(request, "pages/login/perfil.html", context)


def boleta_detalle(request, id):
    try:
        boleta = Boleta.objects.get(id=id)
        detalles = DetalleBoleta.objects.filter(id_boleta=boleta).select_related(
            "producto"
        )
        detalles_list = [
            {
                "producto": {"nombre": detalle.producto.nombre},
                "cantidad": detalle.cantidad,
            }
            for detalle in detalles
        ]
        response_data = {
            "comprador": f"{boleta.comprador.nombre} {boleta.comprador.apellido}",  # Ajusta esto según tus campos
            "fecha": boleta.fecha,
            "total": boleta.total,
            "detalles": detalles_list,
        }
        return JsonResponse(response_data)
    except Boleta.DoesNotExist:
        return JsonResponse({"error": "Boleta no encontrada"}, status=404)


def acceso(request):
    context = {}

    if request.method == "POST":
        if "User" in request.POST and "loginPassword" in request.POST:
            usuario = request.POST.get("User")
            clave = request.POST.get("loginPassword")
            user = authenticate(request, username=usuario, password=clave)
            if user is not None:
                login(request, user)
                return redirect("/home")
            else:
                context["error"] = "Credenciales inválidas. Intente nuevamente."
        elif (
            "registerNombre" in request.POST
            and "registerApellido" in request.POST
            and "registerUsername" in request.POST
            and "registerEmail" in request.POST
            and "registerPassword" in request.POST
            and "registerTelefono" in request.POST
            and "registerRegion" in request.POST
            and "registerComuna" in request.POST
            and "registerDireccion" in request.POST
        ):
            nombre = request.POST.get("registerNombre")
            apellido = request.POST.get("registerApellido")
            nombre_usuario = request.POST.get("registerUsername")
            correo = request.POST.get("registerEmail")
            contraseña = request.POST.get("registerPassword")
            telefono = request.POST.get("registerTelefono")
            region = request.POST.get("registerRegion")
            comuna = request.POST.get("registerComuna")
            direccion = request.POST.get("registerDireccion")

            try:
                if User.objects.filter(email=correo).exists():
                    context["error"] = (
                        "Ya existe un usuario registrado con este correo electrónico. Intente con otro."
                    )
                else:
                    user = User.objects.create_user(
                        username=nombre_usuario,
                        email=correo,
                        password=contraseña,
                        first_name=nombre,
                        last_name=apellido,
                    )
                    user.telefono = telefono
                    user.region = region
                    user.comuna = comuna
                    user.direccion = direccion
                    user.save()

                    login(request, user)
                    return redirect("/home")

            except IntegrityError as e:
                context["error"] = f"Error al registrar usuario: {e}"

    return render(request, "pages/login/acceso.html", context)


def generate_username(request):
    if request.method == "GET":
        adjectives = ["Comfort", "Wood", "Luxury", "Modern", "Classic", "Cozy"]
        nouns = ["Chair", "Table", "Sofa", "Desk", "Shelf", "Couch"]
        random_adjective = random.choice(adjectives)
        random_noun = random.choice(nouns)
        random_number = "".join(random.choices(string.digits, k=3))

        random_username = f"Capibara{random_adjective}{random_noun}{random_number}"
        return JsonResponse({"username": random_username})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/home")


# mercado pago
def process_payment(request):
    if request.method == "POST":
        payment_method_id = request.POST.get("payment_method_id")

        try:
            if payment_method_id.startswith(
                "credit_card"
            ) or payment_method_id.startswith("debit_card"):
                payment = procesar_pago_tarjeta(request)
            else:
                payment = procesar_pago_ticket(request)

            return JsonResponse({"status": "success", "payment": payment})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


def crear_preferencia(request):
    if request.method == "POST":
        transaction_amount = float(request.POST.get("transaction_amount"))

        preference_data = {
            "items": [
                {
                    "title": "Mi producto",
                    "quantity": 1,
                    "unit_price": transaction_amount,
                }
            ],
            "back_urls": {
                "success": "http://127.0.0.1:8000/pago_exitoso/",
                "failure": "http://127.0.0.1:8000/pago_fallido/",
                "pending": "http://127.0.0.1:8000/pago_pendiente/",
            },
            "auto_return": "approved",
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        return JsonResponse({"preference_id": preference["id"]})
