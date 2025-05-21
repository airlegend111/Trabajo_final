import os
import sys
import django

# Añadir el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from datetime import datetime

def update_admin_profile():
    try:
        # Obtener el usuario
        user = User.objects.get(username='Pupu')
        
        # Crear o actualizar el perfil
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.full_name = 'Carlos Andres Baena Moncada'
        profile.role = 'ADMIN'
        profile.save()
        
        print("Perfil de administrador actualizado exitosamente")
        
    except User.DoesNotExist:
        print("Usuario no encontrado")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    update_admin_profile()
