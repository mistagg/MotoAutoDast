from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# STATIC EN AZURE — SIN storage_backends
# ==========================================================

AZURE_ACCOUNT_NAME = os.environ.get("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = os.environ.get("AZURE_ACCOUNT_KEY")
AZURE_STATIC_CONTAINER = "static"

AZURE_CUSTOM_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"

# STATIC URL desde Azure Blob
STATIC_URL = f"https://{AZURE_CUSTOM_DOMAIN}/{AZURE_STATIC_CONTAINER}/"

# Carpeta local que collectstatic llenará ANTES de subir a Azure
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# LOCAL static dir (CSS, JS propios)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Usa el backend simple de Azure Storage para static
STATICFILES_STORAGE = "storages.backends.azure_storage.AzureStorage"

# ==========================================================
# MEDIA LOCAL (NO AZURE)
# ==========================================================
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ==========================================================
# DJANGO CONFIG
# ==========================================================

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'custom_admin',
    'MainApp',
    'widget_tweaks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MotoAutoDast.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MotoAutoDast.wsgi.application'

# ==========================================================
# DATABASE SQLite
# ==========================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==========================================================
# GENERAL
# ==========================================================
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'inicio'

# ==========================================================
# WEBPAY
# ==========================================================
WEBPAY_PLUS_COMMERCE_CODE = os.environ.get("WEBPAY_PLUS_COMMERCE_CODE")
WEBPAY_PLUS_API_KEY = os.environ.get("WEBPAY_PLUS_API_KEY")
WEBPAY_ENV = os.environ.get("WEBPAY_ENV", "TEST")

# ==========================================================
# EMAIL
# ==========================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
