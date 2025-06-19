# 🍎 POS Store Cloud Edition - Grupo 6

**Nombre del proyecto:**
**POS Store Cloud Edition – Despliegue resiliente en AWS para PYMEs chilenas**

---

**Integrantes:**

* Alejandro Robles
* Benjamín Saez
* David Grandon
* Moira Bosman

---

## 📘 Descripción general

Este proyecto es una adaptación del sistema de punto de venta (POS) original de AlgoriSoft, implementado y contenedorizado por el Grupo 6 como parte del módulo de **Cloud Computing y Virtualización**.
La aplicación ha sido rediseñada para funcionar en una arquitectura resiliente sobre AWS, con el objetivo de ofrecer una solución moderna y económica para PYMEs chilenas.

---

## 🧱 Arquitectura implementada

El sistema fue desplegado usando servicios gestionados de AWS:

* 🌐 **Route 53**: Gestión DNS con dominio personalizado `posstore.store`.
* ⚙️ **Amazon EC2**: Instancia con Amazon Linux 2, Docker, Nginx y Gunicorn. Contenedor ejecutando la app Django.
* 🛢️ **Amazon RDS (PostgreSQL)**: Base de datos relacional gestionada, con acceso seguro.
* 🐳 **Docker**: Empaquetado de la aplicación para facilitar despliegues reproducibles.
* ⚖️ **Application Load Balancer (ALB)**: Activo y funcionando correctamente junto a Route 53.

**Nota**: No se utilizó S3 ni backups automáticos en esta versión por decisión técnica y de tiempo.

---

## 🚀 Guía completa de despliegue

### 1️⃣ Conexión a la instancia EC2

```bash
ssh -i "C:\Users\\[TU_USUARIO]\\Desktop\\llave3ev.pem" ec2-user@3.225.77.165
```

### 2️⃣ Preparar entorno EC2

```bash
sudo yum update -y
sudo amazon-linux-extras enable docker
sudo yum install docker git -y
sudo service docker start
sudo usermod -aG docker ec2-user
exit  # Sal y vuelve a entrar para aplicar permisos
```

### 3️⃣ Clonar el repositorio y configurar la app

```bash
git clone https://github.com/ipvg-algoritmos/capacitaci-n-app-docker-grupo-6.git
cd capacitaci-n-app-docker-grupo-6
git pull
```

### 4️⃣ Crear archivo `.env.prod`

```bash
echo "DEBUG=False
SECRET_KEY=tu_clave_secreta
ALLOWED_HOSTS=*
DB_NAME=nombre_base
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=endpoint_de_rds
DB_PORT=5432" > .env.prod
```

### 5️⃣ Build y ejecución del contenedor

```bash
docker build -t pos-store .
docker run -d --env-file .env.prod -p 8000:8000 pos-store
```

### 6️⃣ Comprobación de logs y contenedores

```bash
docker ps
docker logs [ID]
docker rm [ID]
```

### 7️⃣ Limpieza de recursos (opcional)

```bash
docker ps -a
docker system prune -af
docker container prune -f
docker images
docker image prune -f
```

### 8️⃣ Evitar desconexiones en SSH

```bash
ssh -i "C:\Users\\[TU_USUARIO]\\Desktop\\llave3ev.pem" -o ServerAliveInterval=60 ec2-user@3.225.77.165
```

---

## 💻 Despliegue local (Desarrollo)

```bash
git clone https://github.com/ipvg-algoritmos/capacitaci-n-app-docker-grupo-6.git
cd capacitaci-n-app-docker-grupo-6
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate.bat
pip install -r deploy/txt/requirements.txt
python manage.py migrate
python manage.py runserver
```

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
├── deploy/           # Scripts y requerimientos
├── static/           # Archivos estáticos
├── templates/        # Vistas HTML
├── Dockerfile        # Imagen contenedor
├── entrypoint.sh     # Script de entrada
├── .env.prod         # Variables de entorno
├── manage.py         # Utilidad principal de Django
```

---

## 📊 Estado del proyecto

* Aplicación 100% funcional
* Dominio activo: [https://posstore.store](https://posstore.store)
* Accesible desde dispositivos móviles y escritorio
* ALB operativo con Route 53
* SSL activo a través del ALB

---

## 📙 Créditos

* Proyecto base: AlgoriSoft
* Adaptación y despliegue: **Grupo 6 – IPVG**
* Repositorio original: [https://github.com/wdavilav/pos-store](https://github.com/wdavilav/pos-store)

---

## 🎓 Propósito académico

Este proyecto fue desarrollado como parte de la evaluación del módulo de **Cloud Computing y Virtualización**, integrando:

* Arquitectura moderna en AWS
* Contenedores Docker
* Infraestructura como servicio
* Gestión DNS con Route 53
* Trabajo en equipo bajo metodología ágil (Scrum)
