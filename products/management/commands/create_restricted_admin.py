from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from products.models import Pizza
from users.models import Comment

class Command(BaseCommand):
    help = 'Crea un usuario administrador restringido con permisos específicos'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='restricted_admin', type=str)
        parser.add_argument('--password', default='admin123456', type=str)
        parser.add_argument('--email', default='restricted_admin@example.com', type=str)

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        # Crear grupo
        group, _ = Group.objects.get_or_create(name='RestrictedAdmin')
        
        # Asignar permisos para Pizza
        pizza_ct = ContentType.objects.get_for_model(Pizza)
        pizza_perms = Permission.objects.filter(content_type=pizza_ct)
        for perm in pizza_perms:
            group.permissions.add(perm)
            
        # Asignar permisos para Comment
        comment_ct = ContentType.objects.get_for_model(Comment)
        comment_perms = Permission.objects.filter(content_type=comment_ct)
        for perm in comment_perms:
            group.permissions.add(perm)
            
        # Crear usuario
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Usuario {username} creado'))
        else:
            self.stdout.write(self.style.WARNING(f'Usuario {username} ya existe'))
            
        # Añadir al grupo
        user.groups.add(group)
        self.stdout.write(self.style.SUCCESS(f'Usuario {username} añadido al grupo RestrictedAdmin'))
