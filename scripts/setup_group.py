from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from products.models import Pizza
from users.models import Comment

# Crear el grupo RestrictedAdmin
group, created = Group.objects.get_or_create(name='RestrictedAdmin')

# Obtener los content types
pizza_ct = ContentType.objects.get_for_model(Pizza)
comment_ct = ContentType.objects.get_for_model(Comment)

# Obtener todos los permisos para Pizza y Comment
permissions = Permission.objects.filter(content_type__in=[pizza_ct, comment_ct])

# Asignar permisos al grupo
for perm in permissions:
    group.permissions.add(perm)

# Asignar el superusuario al grupo
try:
    admin = User.objects.get(username='ggavi', is_superuser=True)
    admin.groups.add(group)
    print(f"Usuario {admin.username} añadido al grupo RestrictedAdmin")
    print("Permisos asignados:")
    for perm in group.permissions.all():
        print(f"- {perm.codename}")
except User.DoesNotExist:
    print("No se encontró el superusuario ggavi")
