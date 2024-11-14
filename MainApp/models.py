from django.db import models
from decimal import Decimal

# Create your models here.

class Cliente(models.Model):
    nombre_cliente = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    num = models.IntegerField()

    def __str__(self):
        return self.nombre_cliente

class Administrador(models.Model):
    nombre_administrador = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_administrador

class Bodega(models.Model):
    nombre_bodega = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_bodega

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_categoria

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=255)
    descripcion = models.TextField()
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    bodega = models.ForeignKey('Bodega', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    bodega = models.ForeignKey('Bodega', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    costo = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre_producto

class Compra(models.Model):
    fecha_compra = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Compra {self.id} - Cliente: {self.cliente.nombre_cliente}"

class Carro(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_precio_total(self):
        # Asegúrate de que todo sea Decimal antes de multiplicar
        self.precio_total = Decimal(self.cantidad) * Decimal(self.producto.costo)
        self.save()
        
    def __str__(self):
        return f"Carro: {self.producto.nombre_producto} - Cantidad: {self.cantidad}"

class Ingreso(models.Model):
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField()
    cantidad = models.IntegerField()
    precio_costo = models.IntegerField(default=0)

    def __str__(self):
        return f"Ingreso {self.id} - {self.producto.nombre_producto}"

class Contacto(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    asunto = models.CharField(max_length=255)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"