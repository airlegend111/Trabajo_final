import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from products.models import Pizza
from decimal import Decimal

def load_pizzas():
    # Primero, eliminar todas las pizzas existentes
    Pizza.objects.all().delete()
    
    # Leer el archivo SQL
    with open('insert_pizzas.sql', 'r', encoding='utf-8') as file:
        content = file.read()
        # Dividir el contenido en líneas y procesar cada INSERT
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith("('Pizza"):
                # Extraer los valores entre paréntesis
                values = line.strip().strip(',').strip('(').strip(')').split(',')
                
                # Limpiar los valores
                name = values[0].strip().strip("'")
                description = values[1].strip().strip("'")
                size = values[2].strip().strip("'")
                price = Decimal(values[3].strip())
                image = values[4].strip().strip("'")
                
                # Crear la pizza
                Pizza.objects.create(
                    name=name,
                    description=description,
                    size=size,
                    price=price,
                    image=image
                )
                print(f"Created pizza: {name}")

if __name__ == '__main__':
    load_pizzas()
