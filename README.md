# PROYECTO POS STORE - Grupo 6

Sistema de Punto de Venta desarrollado en Django, contenedorizado con Docker y desplegado en AWS como parte del módulo de Cloud Computing.

> 🔧 Fork del proyecto original de AlgoriSoft, adaptado por el Grupo 6 para ser ejecutado en infraestructura cloud escalable con Docker y servicios gestionados de AWS.

---

## 📦 Tecnologías utilizadas

- Python + Django
- PostgreSQL
- Docker
- Amazon EC2
- Amazon RDS
- Application Load Balancer (ALB)
- Amazon S3 (para archivos estáticos y media)
- GitHub Classroom

---

## 🚀 Despliegue en entorno cloud (AWS)

### Arquitectura

- La aplicación Django se ejecuta en un contenedor Docker sobre una instancia EC2.
- El tráfico es balanceado mediante un Application Load Balancer.
- Los datos se almacenan en una base de datos PostgreSQL gestionada en Amazon RDS.
- Los archivos estáticos/media se almacenan en S3.
- La aplicación es monitoreada mediante CloudWatch.

### Requisitos en EC2 (Amazon Linux 2)

```bash
sudo yum update -y
sudo amazon-linux-extras enable docker
sudo yum install docker -y
sudo service docker start
sudo usermod -aG docker ec2-user

