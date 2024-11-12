from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from MainApp.forms import ProductoForm
from .models import Producto, Categoria, Categoria, Bodega, Producto
from .forms import CustomUserCreationForm  # Importa el formulario personalizado

@login_required
def inicio(request):
    productos = Producto.objects.all()  
    return render(request, 'inicio.html', {'productos': productos})

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'catalogoTest.html', {'productos': productos})

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Usa el formulario personalizado
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Hubo un problema al registrarse. Por favor, verifica los datos e intenta nuevamente.')
    else:
        form = CustomUserCreationForm()  # Usa el formulario personalizado
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def Aceites(req):
    try:
        categoria = Categoria.objects.get(nombre_categoria="Aceite")
        productos = Producto.objects.filter(categoria=categoria)
    except Categoria.DoesNotExist:
        productos = []
    return render(req, 'catalogo.html', {'productos': productos, 'categoria': 'Aceite'})

@login_required
def Accesorios(req):
    try:
        categoria = Categoria.objects.get(nombre_categoria="Accesorios")
        productos = Producto.objects.filter(categoria=categoria)
    except Categoria.DoesNotExist:
        productos = []
    return render(req, 'catalogo.html', {'productos': productos, 'categoria': 'Accesorios'})

@login_required
def Neumaticos(req):
    try:
        categoria = Categoria.objects.get(nombre_categoria="Neumaticos")
        productos = Producto.objects.filter(categoria=categoria)
    except Categoria.DoesNotExist:
        productos = []
    return render(req, 'catalogo.html', {'productos': productos, 'categoria': 'Neumáticos'})

@login_required
def Repuestos(req):
    try:
        categoria = Categoria.objects.get(nombre_categoria="Repuestos")
        productos = Producto.objects.filter(categoria=categoria)
    except Categoria.DoesNotExist:
        productos = []
    return render(req, 'catalogo.html', {'productos': productos, 'categoria': 'Repuestos'})

@login_required
def producto_detalle(req, id):
    producto = get_object_or_404(Producto, id=id)
    return render(req, 'producto_detalle.html', {'producto': producto})

def restablecer_contrasena(request):
    return render(request, 'registration/restablecer_contrasena.html', {'mostrar_busqueda': False})

def contacto(request):
    return render(request, 'contacto.html', {'mostrar_busqueda': False})


def buscar_productos(request):
    query = request.GET.get('q')  # Captura el término de búsqueda desde el input "q"
    productos = Producto.objects.filter(nombre_producto__icontains=query) if query else []
    categoria = f"Resultados para '{query}'" if query else "Sin resultados"
    return render(request, 'busqueda.html', {'productos': productos, 'categoria': categoria})

def buscar_productos(request):
    query = request.GET.get('q')  # Captura el término de búsqueda desde el input
    productos = Producto.objects.filter(nombre_producto__icontains=query) if query else []
    categoria = f"Resultados para '{query}'" if query else "Sin resultados"
    return render(request, 'busqueda.html', {'productos': productos, 'categoria': categoria})

def listar_productos(request):
    productos = Producto.objects.all()  # Obtiene todos los productos
    return render(request, 'admin/productos.html', {'productos': productos})


def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')  # Redirige a la lista de productos después de guardar
    else:
        form = ProductoForm()

    # Obtiene las categorías y bodegas de la base de datos
    categorias = Categoria.objects.all()
    bodegas = Bodega.objects.all()

    return render(request, 'admin/agregar_producto.html', {
        'form': form,
        'categorias': categorias,
        'bodegas': bodegas,
    })

def editar_producto(request, producto_id):
    # Obtén el producto a editar
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')  # Redirige a la lista de productos
    else:
        form = ProductoForm(instance=producto)

    # Obtén todas las categorías y bodegas para los select
    categorias = Categoria.objects.all()
    bodegas = Bodega.objects.all()

    return render(request, 'admin/editar_producto.html', {
        'form': form,
        'producto': producto,
        'categorias': categorias,
        'bodegas': bodegas,
    })

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')  # Redirige a la lista de productos después de eliminar

    return render(request, 'admin/confirmar_eliminacion.html', {'producto': producto})