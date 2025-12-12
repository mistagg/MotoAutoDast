from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


# ===============================
# AZURE STORAGE
# ===============================

AZURE_ACCOUNT_NAME = os.environ.get("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = os.environ.get("AZURE_ACCOUNT_KEY")
AZURE_CUSTOM_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"

# --- STATIC ---
STATIC_URL = f"https://{AZURE_CUSTOM_DOMAIN}/static/"
STATICFILES_STORAGE = "MotoAutoDast.storage_backends.AzureStaticStorage"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


# --- MEDIA ---
MEDIA_URL = f"https://{AZURE_CUSTOM_DOMAIN}/media/"
DEFAULT_FILE_STORAGE = "MotoAutoDast.storage_backends.AzureMediaStorage"


# ===============================
# DJANGO BASE
# ===============================

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = ["*"]


# ===============================
# APPS
# ===============================

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


# ===============================
# MIDDLEWARE
# ===============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ===============================
# URLS & WSGI
# ===============================

ROOT_URLCONF = 'MotoAutoDast.urls'
WSGI_APPLICATION = 'MotoAutoDast.wsgi.application'


# ===============================
# TEMPLATES
# ===============================

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

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


# ===============================
# DATABASE
# ===============================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ===============================
# PASSWORD VALIDATION
# ===============================

AUTH_PASSWORD_VALIDATORS = []


# ===============================
# INTERNATIONALIZATION
# ===============================

LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ===============================
# LOGIN / LOGOUT
# ===============================

LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'inicio'


# ===============================
# WEBPAY
# ===============================

WEBPAY_PLUS_COMMERCE_CODE = os.environ.get("WEBPAY_PLUS_COMMERCE_CODE")
WEBPAY_PLUS_API_KEY = os.environ.get("WEBPAY_PLUS_API_KEY")
WEBPAY_ENV = os.environ.get("WEBPAY_ENV", "TEST")


# ===============================
# EMAIL
# ===============================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
