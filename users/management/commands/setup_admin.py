from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile

class Command(BaseCommand):
    help = 'Setup admin user with profile'

    def handle(self, *args, **kwargs):
        try:
            # Obtener o crear el usuario
            user = User.objects.get(username='Pupu')
            
            # Crear o actualizar el perfil
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.full_name = 'Carlos Andres Baena Moncada'
            profile.role = 'ADMIN'
            profile.save()
            
            self.stdout.write(self.style.SUCCESS('Perfil de administrador actualizado exitosamente'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Usuario no encontrado'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
