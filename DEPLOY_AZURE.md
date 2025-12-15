# Guía de Despliegue en Azure App Service

## Problemas Corregidos

### 1. Error de Sintaxis en urls.py
**Error**: Faltaba una coma en la línea 48 del archivo `MotoAutoDast/urls.py`
```python
# ❌ Antes (incorrecto):
path('admin/', include(('custom_admin.urls', 'custom_admin') namespace='admin')),

# ✅ Después (correcto):
path('admin/', include(('custom_admin.urls', 'custom_admin'), namespace='admin')),
```

### 2. DEBUG en Producción
**Problema**: DEBUG estaba hardcodeado a `True` en producción
**Solución**: Ahora se lee correctamente de las variables de entorno

### 3. Archivo startup.sh Faltante
**Problema**: Azure necesita un script de inicio para ejecutar gunicorn
**Solución**: Se creó `startup.sh` con la configuración correcta

---

## Configuración en Azure Portal

### Paso 1: Configurar Variables de Entorno

En Azure Portal, ve a tu App Service > **Configuration** > **Application settings** y agrega:

```
SECRET_KEY = [tu-clave-secreta-segura]
DEBUG = False
ALLOWED_HOSTS = motoautodast-dzgvgmfvcaddgzbs.chilecentral-01.azurewebsites.net
EMAIL_HOST_USER = [tu-email@gmail.com]
EMAIL_HOST_PASSWORD = [tu-app-password]
WEBPAY_PLUS_COMMERCE_CODE = [tu-codigo-comercio]
WEBPAY_PLUS_API_KEY = [tu-api-key]
WEBPAY_ENV = TEST
```

### Paso 2: Configurar el Comando de Inicio

En Azure Portal > **Configuration** > **General settings**:

**Startup Command:**
```bash
bash startup.sh
```

### Paso 3: Configurar el Stack Runtime

En **Configuration** > **General settings**:
- **Stack**: Python
- **Python version**: 3.11 o superior
- **Platform**: Linux

---

## Despliegue desde Git

### Opción A: Despliegue Continuo desde GitHub

1. En Azure Portal, ve a **Deployment Center**
2. Selecciona **GitHub** como fuente
3. Autoriza Azure para acceder a tu repositorio
4. Selecciona:
   - **Organization**: mistagg
   - **Repository**: MotoAutoDast
   - **Branch**: main
5. Guarda la configuración

Azure creará automáticamente un workflow de GitHub Actions.

### Opción B: Despliegue Manual con Git

```bash
# Configura el remote de Azure (obtén la URL del Deployment Center)
git remote add azure https://<deployment-username>@<app-name>.scm.azurewebsites.net/<app-name>.git

# Despliega
git push azure main
```

---

## Comandos Útiles para Debugging

### Ver Logs en Tiempo Real

En Azure Portal > **Log stream** o usando Azure CLI:

```bash
az webapp log tail --name motoautodast --resource-group <tu-resource-group>
```

### SSH al Contenedor

```bash
az webapp ssh --name motoautodast --resource-group <tu-resource-group>
```

### Ejecutar Comandos de Django

```bash
# SSH al contenedor y luego:
cd /home/site/wwwroot
source antenv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

## Verificaciones Post-Despliegue

### 1. Verificar que el Sitio Carga
```
https://motoautodast-dzgvgmfvcaddgzbs.chilecentral-01.azurewebsites.net/
```

### 2. Verificar Archivos Estáticos
- Los archivos CSS, JS e imágenes deben cargar correctamente
- Si no cargan, ejecuta: `python manage.py collectstatic --noinput`

### 3. Verificar Admin Panel
```
https://motoautodast-dzgvgmfvcaddgzbs.chilecentral-01.azurewebsites.net/admin/
```

### 4. Revisar Logs
Busca errores en:
- **Application logs**
- **Web server logs**
- **Detailed error messages**

---

## Problemas Comunes y Soluciones

### Error: "DisallowedHost"
**Síntoma**: `Invalid HTTP_HOST header`
**Solución**: Agrega el dominio de Azure a `ALLOWED_HOSTS` en settings.py o como variable de entorno

### Error: Archivos Estáticos No Cargan
**Solución**:
```bash
# SSH al contenedor
python manage.py collectstatic --noinput
```

### Error: "ModuleNotFoundError"
**Solución**: Verifica que todas las dependencias estén en `requirements.txt`
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Error: Base de Datos
**Problema**: SQLite no persiste en Azure App Service (el sistema de archivos es efímero)
**Solución**: Migrar a Azure Database for PostgreSQL o MySQL

#### Migrar a PostgreSQL en Azure:

1. Crea una Azure Database for PostgreSQL
2. Actualiza `settings.py`:
```python
# Usa PostgreSQL en producción
if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': '5432',
            'OPTIONS': {
                'sslmode': 'require',
            },
        }
    }
```

3. Agrega `psycopg2-binary` a `requirements.txt`
4. Configura las variables de entorno en Azure

---

## Archivos Importantes Creados

### `startup.sh`
Script de inicio que ejecuta:
- Instala dependencias
- Ejecuta collectstatic
- Aplica migraciones
- Inicia Gunicorn

### `.deployment`
Configura Azure para construir durante el despliegue

### `.env.example`
Plantilla de variables de entorno necesarias

---

## Testing Local con Configuración de Producción

```bash
# Activa el entorno virtual
.venv\Scripts\activate

# Configura DEBUG=False localmente
$env:DEBUG="False"
$env:SECRET_KEY="dev-secret-key"

# Ejecuta con gunicorn
gunicorn --bind=127.0.0.1:8000 MotoAutoDast.wsgi:application

# Prueba en: http://127.0.0.1:8000/
```

---

## Checklist Final

- [ ] Variables de entorno configuradas en Azure
- [ ] Comando de inicio configurado: `bash startup.sh`
- [ ] Despliegue continuo configurado
- [ ] Migraciones ejecutadas
- [ ] `collectstatic` ejecutado
- [ ] Sitio carga correctamente
- [ ] Archivos estáticos funcionan
- [ ] Admin panel accesible
- [ ] Considerar migrar a base de datos persistente (PostgreSQL)

---

## Contacto y Soporte

Si encuentras errores, revisa:
1. Application logs en Azure Portal
2. El archivo de logs en `/home/LogFiles/`
3. Ejecuta `python manage.py check` para validar la configuración

## Recursos Adicionales

- [Documentación Django en Azure](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)
- [Azure App Service para Python](https://learn.microsoft.com/en-us/azure/app-service/configure-language-python)
- [WhiteNoise para archivos estáticos](http://whitenoise.evans.io/)
