#!/bin/bash


# Instalar las dependencias
pip install -r requirements.txt

# Realizar migraciones
python manage.py migrate

# Ejecutar el servidor
python manage.py runserver