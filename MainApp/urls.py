from django.contrib import admin
from django.urls import path, include
from MainApp import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('aceites/', views.Aceites, name='lista_aceites'),
    path('accesorios/', views.Accesorios, name='lista_accesorios'),
    path('neumaticos/', views.Neumaticos, name='lista_neumaticos'),
    path('repuestos/', views.Repuestos, name='lista_repuestos'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('producto/<int:id>/', views.producto_detalle, name='producto_detalle'),
]