from django.contrib import admin
from .models import Cliente, Administrador, Bodega, Categoria, Producto, Compra, Carro, Ingreso
from django.utils.html import format_html
# Register your models here.

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_cliente', 'email', 'num')
    search_fields = ('nombre_cliente', 'email')

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_administrador')

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_bodega')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_categoria')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_producto', 'categoria', 'bodega', 'mostrar_imagen')

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.imagen.url)
        return "Sin imagen"

    mostrar_imagen.short_description = 'Imagen'

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_compra', 'cliente')
    list_filter = ('fecha_compra',)
    search_fields = ('cliente__nombre_cliente',)

@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'cantidad', 'precio_total')
    list_filter = ('producto',)
    search_fields = ('producto__nombre_producto',)
    readonly_fields = ('precio_total',)

    def save_model(self, request, obj, form, change):
        # Actualiza el precio total al guardar
        obj.calcular_precio_total()
        super().save_model(request, obj, form, change)

@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('id', 'administrador', 'producto', 'fecha_ingreso', 'cantidad', 'precio_costo')
    list_filter = ('fecha_ingreso', 'administrador')
    search_fields = ('producto__nombre_producto',)
