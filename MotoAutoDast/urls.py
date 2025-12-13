"""
URL configuration for MotoAutoDast project.
... (Resto de comentarios)
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from MainApp.forms import CustomPasswordResetForm 


urlpatterns = [
    # URLs de Administración
    path('admin/', include('custom_admin.urls')), 

    # URLs de Autenticación (Login, Logout)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # URLs Principales
    path('accounts/', include('MainApp.urls')),
    path('', include('MainApp.urls')),    
    
    # URLs de Restablecimiento de Contraseña
    path('restablecer_contrasena/', auth_views.PasswordResetView.as_view(
        form_class=CustomPasswordResetForm,
        template_name='registration/restablecer_contrasena.html',
        email_template_name='password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        html_email_template_name='password_reset_email.html'
    ), name='password_reset'),
    path('restablecer_contrasena/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('restablecer_contrasena/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('restablecer_contrasena/completo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

# ==========================================================
# MANEJO DE ARCHIVOS ESTÁTICOS Y MEDIA EN PRODUCCIÓN
# ==========================================================

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Agregamos los STATICFILES solo si DEBUG es False (Producción)
# Esto resuelve los errores 404/MIME Type en entornos como Azure App Service.
if settings.DEBUG == False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
