# 🍎 POS Store Cloud Edition - Grupo 6

**Nombre del proyecto:**
**POS Store Cloud Edition – Despliegue resiliente en AWS para PYMEs chilenas**

---

## 📘 Descripción general

Este proyecto es una adaptación del sistema de punto de venta (POS) original de AlgoriSoft, implementado y contenedorizado por el Grupo 6 como parte del módulo de **Cloud Computing y Virtualización**.
La aplicación ha sido rediseñada para funcionar en una arquitectura resiliente sobre AWS, permitiendo escalabilidad horizontal, monitoreo, almacenamiento desacoplado y despliegue eficiente a través de contenedores Docker.

El objetivo es ofrecer una solución lista para producción que permita a pequeñas y medianas empresas chilenas utilizar un sistema de ventas robusto, moderno y económico.

---

## 🧱 Arquitectura propuesta (AWS)

El sistema ha sido implementado sobre una arquitectura **cloud-native en EC2**, con los siguientes componentes:

* 🌐 **Route 53**: Gestión DNS con nombre de dominio personalizado
* ⚖️ **Application Load Balancer (ALB)**: Distribución del tráfico entrante a través de zonas de disponibilidad
* 🛣️ **EC2 (Docker Containers)**: Contenedores ejecutando la aplicación Django
* 📃️ **Amazon RDS (PostgreSQL)**: Base de datos relacional administrada
* 📦 **Amazon S3**: Almacenamiento de archivos estáticos y media
* 📊 **CloudWatch**: Monitoreo y visualización de métricas y logs

---

## 🚀 Despliegue en EC2 (Producción)

### 1. Instancia EC2 (Amazon Linux 2)

Conéctate vía SSH e instala Docker:

```bash
sudo yum update -y
sudo amazon-linux-extras enable docker
sudo yum install docker -y
sudo service docker start
sudo usermod -aG docker ec2-user
```

Recuerda cerrar sesión y volver a conectarte para aplicar el grupo docker.

### 2. Clonar el proyecto y construir el contenedor

```bash
git clone https://github.com/ipvg-algoritmos/capacitaci-n-app-docker-grupo-6.git
cd capacitaci-n-app-docker-grupo-6
```

Crea un archivo `.env.prod` con las variables necesarias:

```env
DEBUG=False
SECRET_KEY=tu_clave_secreta
ALLOWED_HOSTS=*
DB_NAME=nombre_base
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=hostname_de_rds
```

Luego ejecuta:

```bash
docker build -t pos-store .
docker run -d --env-file .env.prod -p 8000:8000 pos-store
```

### 3. Configurar puerto y grupo de seguridad

Asegúrate de que tu instancia EC2 permita conexiones entrantes en el puerto 8000 desde el grupo de seguridad del ALB.

El Application Load Balancer debe estar enlazado al Target Group que revisa HTTP:8000.

---

## 💻 Despliegue local (Desarrollo)

### 1. Clona este repositorio

```bash
git clone https://github.com/ipvg-algoritmos/capacitaci-n-app-docker-grupo-6.git
cd capacitaci-n-app-docker-grupo-6
```

### 2. Crea y activa el entorno virtual

```bash
python -m venv venv
venv\Scripts\activate.bat        # Windows
# o
source venv/bin/activate         # Linux/macOS
```

### 3. Instala las dependencias

```bash
pip install -r deploy/txt/requirements.txt
```

### 4. Migraciones y carga inicial

```bash
python manage.py migrate
python manage.py shell --command='from core.init import *'
python manage.py shell --command='from core.utils import *'   # Opcional
```

### 5. Ejecuta el servidor local

```bash
python manage.py runserver
```

Visita: [http://localhost:8000](http://localhost:8000)

---

## 🔐 Credenciales de prueba

```bash
username: admin
password: hacker94
```

---

## 📁 Estructura del proyecto

```
├── config/           # Configuración global Django
├── core/             # Módulo principal del POS
├── deploy/           # Requerimientos y scripts de instalación
├── static/           # Archivos estáticos
├── templates/        # Vistas HTML
├── Dockerfile        # Imagen para contenedor
├── entrypoint.sh     # Script de entrada del contenedor
├── .env.prod         # Variables de entorno para producción
├── manage.py         # Utilidad de Django
```

---

## 📙 Créditos

* Proyecto base: AlgoriSoft en YouTube
* Adaptación cloud y contenedorización: **Grupo 6 – IPVG**
* Repositorio original: `https://github.com/wdavilav/pos-store`

---

## 🧠 Propósito académico

Este proyecto fue desarrollado como parte de la evaluación del módulo de **Cloud Computing y Virtualización**, integrando:

* Arquitectura cloud moderna
* Contenedores Docker
* Gestión de infraestructura en AWS
* Metodología de trabajo ágil (Scrum)

