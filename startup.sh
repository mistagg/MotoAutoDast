#!/bin/bash

# Activar entorno virtual si existe
if [ -d "antenv" ]; then
    source antenv/bin/activate
fi

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar collectstatic (con --noinput para no pedir confirmación)
python manage.py collectstatic --noinput

# Ejecutar migraciones
python manage.py migrate

# Iniciar Gunicorn
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers=4 MotoAutoDast.wsgi:application
