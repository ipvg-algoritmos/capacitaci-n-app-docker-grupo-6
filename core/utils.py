import json
import os
import random
import string
from datetime import date

import django
from django.db.utils import IntegrityError

from config import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.pos.models import Product, Category, Client, SaleDetail, Sale, Company
from core.user.models import User


def insert_data():
    numbers = list(string.digits)

    # Empresa
    if not Company.objects.exists():
        company = Company(
            name='POS-STORE S.A.',
            ruc='0928363993001',
            address='MILAGRO, CDLA PAQUISHA',
            mobile='0996555528',
            phone='2977557',
            email='williamjair94@hotmail.com',
            website='https://algorisoft.com',
            description='VENTA AL POR MAYOR Y MENOS DE PRODUCTOS DE PRIMERA NECESIDAD',
            iva=12.00
        )
        company.save()
        print("✅ Empresa insertada")
    else:
        print("🔁 Empresa ya existente")

    # Productos
    try:
        with open(f'{settings.BASE_DIR}/deploy/json/products.json', encoding='utf8') as json_file:
            for item in json.load(json_file):
                if not Product.objects.filter(code=item['code']).exists():
                    category, _ = Category.objects.get_or_create(name=item['category'])
                    product = Product(
                        name=item['name'],
                        code=item['code'],
                        category=category,
                        price=float(item['price']),
                        pvp=float(item['pvp']),
                        stock=random.randint(50, 150)
                    )
                    product.save()
                    print(f'✅ Producto insertado: {product.name}')
                else:
                    print(f'🔁 Producto ya existente: {item["code"]}')
    except FileNotFoundError:
        print("❌ No se encontró el archivo de productos.")

    # Servicio único
    if not Product.objects.filter(code='FORMATEO85451').exists():
        category, _ = Category.objects.get_or_create(name='SERVICIOS')
        Product.objects.create(
            name='FORMATEO DE COMPUTADORAS',
            category=category,
            is_service=True,
            with_tax=False,
            pvp=15.00,
            code='FORMATEO85451'
        )
        print("✅ Servicio insertado")
    else:
        print("🔁 Servicio ya existente")

    # Cliente "Consumidor Final"
    if not Client.objects.filter(dni='9999999999999').exists():
        Client.objects.create(
            names='Consumidor Final',
            dni='9999999999999',
            email='davilawilliam94@gmail.com',
            birthdate=date(1994, 10, 19),
            mobile='9999999999',
            address='Milagro, cdla. Paquisha'
        )
        print("✅ Cliente 'Consumidor Final' insertado")
    else:
        print("🔁 Cliente 'Consumidor Final' ya existe")

    # Clientes desde JSON
    try:
        with open(f'{settings.BASE_DIR}/deploy/json/customers.json', encoding='utf8') as json_file:
            data = json.load(json_file)
            for item in data[0:20]:
                email = item['email']
                if not Client.objects.filter(email=email).exists():
                    client = Client(
                        names=f"{item['first']} {item['last']}",
                        dni=''.join(random.choices(numbers, k=10)),
                        birthdate=date(random.randint(1969, 2006), random.randint(1, 12), random.randint(1, 28)),
                        mobile=''.join(random.choices(numbers, k=10)),
                        email=email,
                        address=item['country']
                    )
                    client.save()
                    print(f'✅ Cliente insertado: {client.names}')
                else:
                    print(f'🔁 Cliente ya existe: {email}')
    except FileNotFoundError:
        print("❌ No se encontró el archivo de clientes.")

    # Ventas aleatorias (si hay clientes y productos)
    client_ids = list(Client.objects.values_list('id', flat=True))
    product_ids = list(Product.objects.values_list('id', flat=True))

    if not client_ids or not product_ids:
        print("❌ No hay clientes o productos disponibles para generar ventas.")
        return

    employee = User.objects.first()
    if not employee:
        print("❌ No se encontró ningún usuario para registrar ventas.")
        return

    for _ in range(random.randint(6, 10)):
        sale = Sale(
            company_id=1,
            employee_id=employee.id,
            client_id=random.choice(client_ids),
            iva=0.12
        )
        sale.save()

        for _ in range(1, 8):
            available_products = Product.objects.filter(stock__gt=0)
            if not available_products.exists():
                continue

            product = random.choice(available_products)
            cant = random.randint(1, max(1, int(product.stock * 0.3)))

            detail = SaleDetail(
                sale=sale,
                product=product,
                cant=cant,
                price=product.pvp
            )
            detail.save()

            product.stock -= cant
            product.save()

        sale.calculate_detail()
        sale.calculate_invoice()
        sale.cash = sale.total
        sale.save()
        print(f'✅ Venta insertada: {sale.id}')


insert_data()
