from django.db import models


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

    def __str__(self):
        txt = "[{0}] {1} - {2}"
        return txt.format(self.cod, self.mueble, self.nombre)


class Cargo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)

    def __str__(self):
        txt = "[{0}] {1}"
        return txt.format(self.id, self.nombre)


class User(models.Model):
    username = models.CharField(primary_key=True, max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, null=False)
    nombre = models.CharField(max_length=50, null=False)
    direccion = models.CharField(max_length=100, null=False)
    telefono = models.IntegerField(null=False)
    subscribed = models.BooleanField(null=False, default=False)
    tipo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

    def __str__(self):
        txt = "[{0}] {1}"
        return txt.format(self.username, self.nombre)


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
    comprador = models.ForeignKey(User, on_delete=models.CASCADE)
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
