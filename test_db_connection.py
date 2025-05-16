import os
import django

# Configurar Django antes de usar el módulo de conexión
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bigotes_pizzeria.settings')
django.setup()

from django.db import connection

def test_connection():
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        row = cursor.fetchone()
        print(row)

if __name__ == "__main__":
    test_connection()