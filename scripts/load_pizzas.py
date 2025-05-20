import os
import django
import sys
import re

# Configurar el entorno de Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from products.models import Pizza

def parse_sql_file():
    sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'insert_pizzas.sql')
    with open(sql_path, 'r', encoding='utf-8') as sql_file:
        sql_content = sql_file.read()
    
    # Extraer los valores usando expresiones regulares
    pattern = r"\('([^']*)', '([^']*)', '([^']*)', ([0-9.]*), ([^)]*)\)"
    matches = re.findall(pattern, sql_content)
    
    return [
        {
            'name': name,
            'description': description,
            'size': size,
            'price': float(price)
        }
        for name, description, size, price, _ in matches
    ]

def load_pizzas():
    pizzas_data = parse_sql_file()
    
    # Primero, eliminar todas las pizzas existentes para evitar duplicados
    Pizza.objects.all().delete()
    
    # Crear las nuevas pizzas
    pizzas_created = []
    for pizza_data in pizzas_data:
        pizza = Pizza(**pizza_data)
        pizzas_created.append(pizza)
    
    # Usar bulk_create para inserción eficiente
    Pizza.objects.bulk_create(pizzas_created)
    print(f"Se han creado {len(pizzas_created)} pizzas exitosamente.")

if __name__ == '__main__':
    load_pizzas()
