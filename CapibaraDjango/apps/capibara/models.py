from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    img = models.ImageField(upload_to="imgCategorias", null=True, blank=True)

    def __str__(self):
        txt = "[{0}] {1}"
        return txt.format(self.id, self.nombre)


class Mueble(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)

    def __str__(self):
        txt = "[{0}] {1}"
        return txt.format(self.id, self.nombre)


class User(AbstractUser):
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    username = models.CharField(primary_key=True, max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=50, null=False)
    telefono = models.CharField(max_length=12, null=False)
    region = models.CharField(max_length=100, null=False)
    comuna = models.CharField(max_length=100, null=False)
    direccion = models.CharField(max_length=100, null=False)
    subscribed = models.BooleanField(null=False, default=False)
    preference_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        txt = "[{0}] {1}"
        return txt.format(self.username, self.nombre)


class Producto(models.Model):
    img = models.ImageField(upload_to="imgProductos")
    cod = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    clasificacion = models.CharField(max_length=100, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    mueble = models.ForeignKey(Mueble, on_delete=models.CASCADE)
    stock = models.IntegerField(null=False)
    precio = models.IntegerField(null=False, default=0)
    descripcion = models.TextField(blank=True, null=True)
    fecha_ingreso = models.DateField(auto_now_add=True)
    ventas = models.IntegerField(default=0)

    # Medidas del producto
    largo_cm = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    ancho_cm = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )
    alto_cm = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )

    # Materiales y accesorios
    cantidad_planchas = models.IntegerField(default=0, blank=False)
    cantidad_tornillos = models.IntegerField(default=0, blank=False)
    # Repuestos
    cantidad_manillas = models.IntegerField(default=0, blank=False)
    cantidad_bisagras = models.IntegerField(default=0, blank=False)
    cantidad_patas_gomas = models.IntegerField(default=0, blank=False)
    cantidad_rieles = models.IntegerField(default=0, blank=False)

    disponible = models.BooleanField(default=True)

    def decrementar_stock(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
            if self.stock == 0:
                self.disponible = False
            self.save()
        else:
            raise ValueError("No hay suficiente stock para decrementar.")

    def __str__(self):
        txt = "[{0}] {1} - {2}"
        return txt.format(self.cod, self.mueble, self.nombre)


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Usuario que hizo el pedido
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(
        upload_to="imgOrden", null=True, blank=True
    )  # Allow null and blank

    def save(self, *args, **kwargs):
        if not self.id:  # Only copy the image when creating a new OrderItem
            self.image = self.product.img
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.nombre} - {self.order}"


class Opinion(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="opiniones"
    )
    username = models.CharField(max_length=100)
    calificacion = models.IntegerField()
    comentario = models.TextField()

    def __str__(self):
        return f"Opinión de {self.username} sobre {self.producto}"


class Boleta(models.Model):
    id = models.AutoField(primary_key=True)
    comprador = models.ForeignKey(
        User, related_name="boletas", on_delete=models.CASCADE
    )
    fecha = models.DateField(auto_now_add=True)
    total = models.IntegerField(null=False)
    estado = models.CharField(max_length=20, null=False, default="Por enviar")

    def __str__(self):
        txt = "[Boleta N°{0}] Comprador: {1}"
        return txt.format(self.id, self.comprador)


class DetalleBoleta(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(null=False)

    def __str__(self):
        txt = "[Detalle {0}] {1} x {2}"
        return txt.format(self.id_boleta, self.producto, self.cantidad)
