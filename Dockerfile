FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libglib2.0-dev \
    libxml2 \
    libxslt1.1 \
    pkg-config \
    python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python
COPY deploy/txt/requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo el proyecto
COPY . .

# 🔧 Corrige rutas en CSS con comillas que rompen ManifestStaticFilesStorage
RUN find ./static/lib -type f -name "*.css" -exec sed -i 's/url("images\//url(images\//g' {} + \
 && find ./static/lib -type f -name "*.css" -exec sed -i "s/url('images\//url(images\//g" {} +

# Permite servir archivos estáticos desde WhiteNoise
RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

# Copia y da permisos al script de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
