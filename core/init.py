import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.security.models import *
from django.contrib.auth.models import Permission
from django.db.utils import IntegrityError

from core.pos.models import *
from core.user.models import User

# Crear dashboard si no existe
try:
    dashboard = Dashboard()
    dashboard.name = 'INVOICE WEB'
    dashboard.icon = 'fas fa-shopping-cart'
    dashboard.author = 'William Jair Dávila Vargas'
    dashboard.save()
    print("✅ Dashboard creado")
except IntegrityError:
    print("🔁 Ya existía el dashboard")

# Crear grupo si no existe
group, created = Group.objects.get_or_create(name='Administrador')
if created:
    print(f'✅ insertado grupo: {group.name}')
else:
    print(f'🔁 Ya existía el grupo: {group.name}')

# Asignar permisos al grupo
for permission in Permission.objects.exclude(content_type__app_label__in=['admin', 'auth', 'contenttypes', 'sessions']):
    group.permissions.add(permission)

# Crear usuario admin si no existe
if not User.objects.filter(username='admin').exists():
    user = User()
    user.names = 'William Jair Dávila Vargas'
    user.username = 'admin'
    user.email = 'davilawilliam93@gmail.com'
    user.is_active = True
    user.is_superuser = True
    user.is_staff = True
    user.set_password('hacker94')
    user.save()
    user.groups.add(group)
    print(f'✅ Usuario {user.names} creado con éxito')
else:
    print("🔁 Usuario admin ya existe")
