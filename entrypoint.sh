#!/bin/bash

echo "🔧 Creando migraciones de apps locales..."
python manage.py makemigrations user
python manage.py makemigrations security
python manage.py makemigrations pos

echo "✅ Aplicando migraciones..."
python manage.py migrate --noinput

echo "📥 Insertando datos iniciales del sistema (usuarios y roles)..."
python manage.py shell -c 'from core.init import *'

echo "📊 Insertando datos aleatorios (clientes, productos, ventas)..."
python manage.py shell -c 'from core.utils import *'

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
  echo "❌ Error: Falló la recolección de archivos estáticos."
  exit 1
fi


echo "🚀 Iniciando servidor con Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
