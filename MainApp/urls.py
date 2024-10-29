from django.contrib import admin
from django.urls import path, include
from MainApp import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('accounts/', include('django.contrib.auth.urls')),

]