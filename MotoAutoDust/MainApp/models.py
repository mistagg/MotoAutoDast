from django.db import models

# Create your models here.

class Cliente(models.Model):
    id_cliente = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=255)
    Email = models.CharField(max_length=255)
    numero = models.CharField(max_length=9)
    
    
class Compra(models.Model):
    id_compra = models.IntegerField(unique=True)
    fecha_compra = models.DateField()
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"