# Configuración Azure - MotoAutoDast

## ⚠️ PASOS CRÍTICOS PARA EVITAR ERROR 500 EN /admin/

### 1. Variables de Entorno en Azure
En Azure Portal > App Service > Configuration > Application settings, agregar:

```
DEBUG = False
SECRET_KEY = <tu-clave-secreta-larga-y-aleatoria>
ALLOWED_HOSTS = motoautodast-dzgvgmfvcaddgzbs.chilecentral-01.azurewebsites.net

# Email
EMAIL_HOST_USER = <tu-email>
EMAIL_HOST_PASSWORD = <tu-password-app>

# Webpay (opcional si usas TEST)
WEBPAY_PLUS_COMMERCE_CODE = <tu-codigo>
WEBPAY_PLUS_API_KEY = <tu-api-key>
WEBPAY_ENV = PRODUCTION
```

### 2. Comandos Post-Deploy en Azure
En Azure Portal > App Service > Configuration > General Settings > Startup Command:

```bash
python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind=0.0.0.0 --timeout 600 MotoAutoDast.wsgi
```

### 3. Crear Superusuario en Azure
Conectarse a SSH de Azure y ejecutar:
```bash
python manage.py createsuperuser
```

### 4. Verificar Logs
Si sigue dando error 500, revisar logs en:
Azure Portal > App Service > Log stream

## 🔍 Problemas Comunes Solucionados

1. ✅ **STATICFILES_DIRS** - Ahora valida si la carpeta existe
2. ✅ **LOGGING** - Agregado para ver errores en Azure
3. ✅ **Manejo de excepciones** - En admin_login y dashboard
4. ✅ **WhiteNoise** - Configurado correctamente para archivos estáticos
5. ✅ **CSRF_TRUSTED_ORIGINS** - Ya incluye tu dominio Azure

## 📦 Base de Datos
Actualmente usa SQLite. Para producción considera migrar a:
- Azure Database for PostgreSQL
- Azure SQL Database

## 🚀 Deploy desde Git
```bash
git add .
git commit -m "Fix: Corregido error 500 en /admin/ para Azure"
git push origin main
```

Azure detectará los cambios y redesplegará automáticamente.
