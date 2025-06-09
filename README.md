# 🍎 POS Store Cloud Edition - Grupo 6

**Nombre del proyecto:**  
**POS Store Cloud Edition – Despliegue resiliente en AWS para PYMEs chilenas**

---

**Integrantes:**  
- Alejandro Robles  
- Benjamín Saez  
- David Grandon  
- Moira Bosman  

---

## 📘 Descripción general

Este proyecto es una adaptación del sistema de punto de venta (POS) original de AlgoriSoft, implementado y contenedorizado por el Grupo 6 como parte del módulo de **Cloud Computing y Virtualización**.  
La aplicación ha sido rediseñada para funcionar en una arquitectura resiliente sobre AWS, con el objetivo de ofrecer una solución moderna y económica para PYMEs chilenas.

---

## 🧱 Arquitectura implementada

El sistema fue desplegado usando servicios gestionados de AWS:

- 🌐 **Route 53**: Gestión DNS con dominio personalizado `posstore.store`.
- ⚙️ **Amazon EC2**: Instancia con Amazon Linux 2, Docker, Nginx y Gunicorn. Contenedor ejecutando la app Django.
- 🛢️ **Amazon RDS (PostgreSQL)**: Base de datos relacional gestionada, con acceso seguro.
- 🐳 **Docker**: Empaquetado de la aplicación para facilitar despliegues reproducibles.
- ⚖️ **Application Load Balancer (ALB)**: Configurado, pero no activo por estado "unhealthy". Se utiliza IP elástica temporalmente.

**Nota**: No se utilizó S3 ni backups automáticos en esta versión por decisión técnica y de tiempo.

---

## 🚀 Despliegue en EC2 (Producción)

```bash
# Conexión a EC2
ssh -i "C:\Users\aleja\OneDrive\Desktop\llave3ev.pem" ec2-user@3.225.77.165

# Preparar entorno
sudo yum update -y
sudo amazon-linux-extras enable docker
sudo yum install docker git -y
sudo service docker start
sudo usermod -aG docker ec2-user
exit  # volver a entrar

# Clonar y desplegar la app
git clone https://github.com/ipvg-algoritmos/capacitaci-n-app-docker-grupo-6.git
cd capacitaci-n-app-docker-grupo-6

# Crear archivo .env.prod
echo "DEBUG=False
SECRET_KEY=tu_clave_secreta
ALLOWED_HOSTS=*
DB_NAME=nombre_base
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=hostname_de_rds" > .env.prod

# Construir y correr
docker build -t pos-store .
docker run -d --env-file .env.prod -p 8000:8000 pos-store

# Comandos útiles
git pull
docker logs [ID]
docker ps -a
docker container prune -f
docker image prune -f

# Evitar desconexiones
ssh -i "C:\Users\aleja\OneDrive\Desktop\llave3ev.pem" -o ServerAliveInterval=60 ec2-user@3.225.77.165
```

---

## 💻 Despliegue local (Desarrollo)

```bash
# Clonar el proyecto
git clone https://github.com/ipvg-algoritmos/capacitaci-n-app-docker-grupo-6.git
cd capacitaci-n-app-docker-grupo-6

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate.bat

# Instalar dependencias
pip install -r deploy/txt/requirements.txt

# Migraciones y carga inicial
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

- Aplicación 100% funcional
- Dominio activo: [https://posstore.store](https://posstore.store)
- Accesible desde dispositivos móviles y escritorio
- Sin necesidad de entornos locales para ejecución
- ALB no operativo (se usa IP directa)
- SSL pendiente (requiere ALB funcional)

---

## 📙 Créditos

- Proyecto base: AlgoriSoft
- Adaptación y despliegue: **Grupo 6 – IPVG**
- Repositorio original: https://github.com/wdavilav/pos-store

---

## 🎓 Propósito académico

Este proyecto fue desarrollado como parte de la evaluación del módulo de **Cloud Computing y Virtualización**, integrando:

- Arquitectura moderna en AWS
- Contenedores Docker
- Infraestructura como servicio
- Gestión DNS con Route 53
- Trabajo en equipo bajo metodología ágil (Scrum)
