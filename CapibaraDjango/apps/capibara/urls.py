from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path("", views.CargarHome),
    path("home", views.CargarHome, name="home"),
    path("ver_producto/<int:p_cod>/", views.ver_producto, name="ver_producto"),
    path("productos", views.CargarProductos, name="productos"),
    # almacenar confirmar
    path("contacto", views.CargarContacto, name="contacto"),
    # carrito
    path("carrito", views.CargarCarrito, name="carrito"),
    path("agregar-al-carrito/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path(
        "eliminar-producto/<int:cod_producto>/",
        views.eliminar_producto,
        name="eliminar_producto",
    ),
    path("vaciar-carrito/", views.vaciar_carrito, name="vaciar_carrito"),
    # agregar opiniones para los productos
    path("agregar-opinion/<int:p_cod>", views.agregar_opinion, name="agregar_opinion"),
    # Redireccion para las paginas
    path("cocina/", views.CargarCocina, name="cocina"),
    path("comedor/", views.CargarComedor, name="comedor"),
    path("dormitorio/", views.CargarDormitorio, name="dormitorio"),
    # Login/registro
    path("acceso", views.acceso, name="acceso"),
    path("generate-username/", views.generate_username, name="generate-username"),
    # logout
    path("logout/", logout_view, name="logout"),
    path("perfil/", views.perfil, name="perfil"),
    path("boleta/<int:id>/", views.boleta_detalle, name="boleta_detalle"),
    # mercadopago
    path("process_payment/", views.process_payment, name="process_payment"),
    path("crear_preferencia/", views.crear_preferencia, name="crear_preferencia"),
]
