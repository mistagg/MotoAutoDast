from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Producto
# Create your views here.

@login_required
def inicio(req):
    return render(req, 'inicio.html')

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'catalogoTest.html', {'productos': productos})