from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Sum
from MainApp.models import Compra, Producto, Categoria, Cliente
from django.db.models import Sum, Count
from django.utils import timezone
from MainApp.models import Visita

def admin_login(req):
    try:
        if req.user.is_authenticated:
            if req.user.is_staff:
                return redirect('/admin/dashboard/')
            else:
                return redirect('/')

        if req.method == 'POST':
            username = req.POST.get('username')
            password = req.POST.get('password')

            user_obj = authenticate(username=username, password=password)

            if user_obj:
                if user_obj.is_staff:
                    login(req, user_obj)
                    return redirect('/admin/dashboard/')
                else:
                    messages.info(req, 'No tienes permiso para acceder a esta sección')
                    return redirect('/')
            else:
                messages.info(req, 'Usuario o contraseña incorrectos')
                return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

        return render(req, 'admin/Adminlogin.html')

    except Exception as e:
        print("Error:", e)
        messages.error(req, 'Error inesperado al intentar iniciar sesión')
        return redirect('/')




@login_required
def dashboard(req):

    # Solo superusuarios pueden entrar
    if not req.user.is_superuser:
        return redirect('/')

    # ------------------- TARJETAS SUPERIORES -------------------

    # Pedidos Pendientes
    total_pedidos_pendientes = Compra.objects.filter(estado='pendiente').count()

    # Pedidos Enviados
    total_pedidos_enviados = Compra.objects.filter(estado='enviado').count()

    # Ventas Totales
    total_ventas = Compra.objects.filter(
        estado='enviado'
    ).aggregate(
        total=Sum('monto')
    )['total'] or 0

    # ------------------- VISITAS POR MES -------------------

    meses_labels = [
        "Enero","Febrero","Marzo","Abril","Mayo","Junio",
        "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
    ]

    visitas_data = [
        Visita.objects.filter(fecha__month=i).count() for i in range(1, 13)
    ]

    # ------------------- CATEGORÍAS MÁS VISTAS -------------------

    categorias_labels = []
    categorias_valores = []

    for categoria in Categoria.objects.all():
        visitas_categoria = Visita.objects.filter(
            producto__categoria=categoria
        ).count()

        categorias_labels.append(str(categoria.nombre_categoria))
        categorias_valores.append(int(visitas_categoria))

    # ------------------- CONTEXTO -------------------

    context = {
        "total_pedidos_pendientes": total_pedidos_pendientes,
        "total_pedidos_enviados": total_pedidos_enviados,
        "total_ventas": total_ventas,
        "meses_labels": meses_labels,
        "visitas_data": visitas_data,
        "categorias_labels": categorias_labels,
        "categorias_valores": categorias_valores,
    }

    return render(req, "admin/dashboard.html", context)

@login_required
def pagos_view(request):
    if not request.user.is_superuser:
        return redirect('/')
    pagos = Compra.objects.select_related('cliente').order_by('-fecha_compra')
    return render(request, 'admin/pagos.html', {'pagos': pagos})


def ajustes(request):
    return render(request, 'admin/ajustes.html')
