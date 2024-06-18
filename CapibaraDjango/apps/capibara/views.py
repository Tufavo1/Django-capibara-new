from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
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
from django.views.decorators.csrf import csrf_exempt
import json


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
        "pages/productos/cocina.html",
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
        "pages/productos/dormitorio.html",
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

    return render(request, "pages/login/perfil.html", context)


# Historial de productos comprados
@login_required
def order_history(request):
    orders = Order.objects.filter(
        user=request.user
    )  # Get orders for the logged-in user
    context = {"orders": orders}
    return render(request, "pages/login/perfil.html", context)


@csrf_exempt
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
                pass
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
                        nombre=nombre,
                        apellido=apellido,
                        telefono=telefono,
                        region=region,
                        comuna=comuna,
                        direccion=direccion,
                    )

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
@csrf_exempt
@login_required
def process_payment(request):
    if request.method == "POST":
        try:
            form_data = json.loads(request.body)
            transaction_amount = form_data.get("transaction_amount")
            items = form_data.get("items")

            if items is None or transaction_amount is None:
                return JsonResponse(
                    {"error": "Datos incompletos en la solicitud"}, status=400
                )

            # Crear la orden
            order = Order.objects.create(
                user=request.user, total_amount=transaction_amount
            )

            del request.session["carrito"]
            request.session.modified = True

            # Crear los items de la orden y decrementar el stock
            for item in items:
                producto = get_object_or_404(Producto, cod=item["cod"])
                OrderItem.objects.create(
                    order=order,
                    product=producto,
                    quantity=item["cantidad"],
                    price=item["precio"],
                    image=item[
                        "imagen"
                    ],  # Utiliza la imagen proporcionada en el carrito
                )

                # Decrementar el stock del producto
                try:
                    producto.decrementar_stock(item["cantidad"])
                except ValueError as e:
                    # Manejar el error de stock insuficiente, si es necesario
                    return JsonResponse({"error": str(e)}, status=400)
            # Payment Successful - Update Order Status
            order.status = "processing"
            order.save()
            # Redirigir a la página de pago exitoso con la orden ID
            return JsonResponse({"redirect_url": f"/pago_exitoso/{order.id}/"})
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Error al decodificar los datos JSON"}, status=400
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método de solicitud no permitido"}, status=405)


@login_required
def crear_preferencia(request):
    if request.method == "POST":
        data = json.loads(request.body)
        transaction_amount = data.get("transaction_amount")
        items = data.get("items")

        # Obtener información del usuario autenticado
        user = request.user
        payer_info = {
            "name": user.first_name,
            "surname": user.last_name,
            "email": user.email,
        }

        preference_items = []
        for item in items:
            preference_items.append(
                {
                    "title": item["nombre"],
                    "quantity": item["cantidad"],
                    "unit_price": item["precio"],
                    "picture_url": item["imagen"],
                }
            )

        preference_data = {
            "items": preference_items,
            "payer": payer_info,
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


@login_required
def cargar_pago_exitoso(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {"order": order, "items": order.items.all()}
    return render(request, "pages/mercadopago/pago_exitoso.html", context)


def CargarPagofallido(request):
    return render(request, "pages/mercadopago/fallido.html")


def CargarPagopendiente(request):
    return render(request, "pages/mercadopago/exito.html")
