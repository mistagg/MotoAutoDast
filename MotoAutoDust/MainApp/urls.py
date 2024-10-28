from django.contrib import admin
from django.urls import path, include
from MainApp import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('accounts/', include('django.contrib.auth.urls')),

]