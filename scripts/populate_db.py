import os
import django
import random
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from products.models import Product

def populate_products():
    """
    Populates the database with 100 sample products.
    """
    products = []
    for i in range(100):
        product = Product(
            name=f"Producto {i+1}",
            description=f"Descripción del producto {i+1}. Este es un producto de ejemplo.",
            price=Decimal(random.uniform(10.0, 100.0)).quantize(Decimal('0.01')),
        )
        products.append(product)
    
    Product.objects.bulk_create(products)
    print("100 productos creados exitosamente.")

if __name__ == "__main__":
    populate_products()