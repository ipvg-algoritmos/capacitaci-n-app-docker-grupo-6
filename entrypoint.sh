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

echo "🩺 Verificando ruta de salud..."
HEALTH_ROUTE_FILE="config/health_url.py"
if ! grep -q "path(\"health/" config/urls.py; then
  echo "🔧 Agregando ruta de /health automáticamente"
  echo 'from django.http import HttpResponse' > "$HEALTH_ROUTE_FILE"
  echo 'health_view = lambda request: HttpResponse("OK")' >> "$HEALTH_ROUTE_FILE"
  echo '' >> "$HEALTH_ROUTE_FILE"
  echo 'urlpatterns.append(path("health/", health_view, name="health"))' >> "$HEALTH_ROUTE_FILE"

  # Agrega include dinámico si no existe
  echo 'from config import health_url' >> config/urls.py
fi

echo "🚀 Iniciando servidor con Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
