import os
import django
from django.core.files import File
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bigotes_pizzeria.settings')
django.setup()

from pizzeria.models import Pizza
from django.contrib.auth.models import User

# Crear superusuario
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')

# Crear 100 pizzas
Pizza.objects.all().delete()  # Limpiar la tabla antes de insertar
for i in range(1, 101):
    pizza = Pizza(
        name=f'Pizza {i}',
        description=f'Deliciosa pizza número {i} con ingredientes frescos.',
        price=Decimal('10.99') + Decimal(i),
    )
    # Asignar una imagen estática (opcional)
    try:
        with open('pizzeria/static/img/pizza1.webp', 'rb') as img_file:
            pizza.image.save(f'pizza{i}.webp', File(img_file), save=True)
    except FileNotFoundError:
        print("Imagen no encontrada, se creará la pizza sin imagen.")
    pizza.save()
print("100 pizzas creadas exitosamente.")