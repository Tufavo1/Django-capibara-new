from django.urls import path
from . import views
from .views import  logout_view

urlpatterns = [
    path("", views.CargarHome),
    path("home", views.CargarHome, name="home"),
    path("ver_producto/<int:p_cod>/", views.ver_producto, name="ver_producto"),
    path("productos", views.CargarProductos, name="productos"),
    path("contacto", views.CargarContacto, name="contacto"),
    # carrito
    path("carrito", views.CargarCarrito, name="carrito"),
    path("agregar-al-carrito/", views.agregar_al_carrito, name="agregar_al_carrito"),
    # agregar opiniones para los productos
    path("agregar-opinion/<int:p_cod>", views.agregar_opinion, name="agregar_opinion"),
    # Redireccion para las paginas
    path("cocina/", views.CargarCocina, name="cocina"),
    path("comedor/", views.CargarComedor, name="comedor"),
    path("dormitorio/", views.CargarDormitorio, name="dormitorio"),

    #Login/registro
    path('acceso', views.acceso, name='acceso'),

    #logout
    path('logout/', logout_view, name='logout'),
]
