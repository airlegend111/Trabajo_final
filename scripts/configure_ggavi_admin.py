from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from products.models import Pizza
from users.models import Comment

def setup_admin_user():
    # 1. Obtener o crear el grupo RestrictedAdmin
    restricted_group, _ = Group.objects.get_or_create(name='RestrictedAdmin')
    
    # 2. Obtener los content types para los modelos
    pizza_ct = ContentType.objects.get_for_model(Pizza)
    comment_ct = ContentType.objects.get_for_model(Comment)
    
    # 3. Obtener todos los permisos necesarios
    pizza_permissions = Permission.objects.filter(content_type=pizza_ct)
    comment_permissions = Permission.objects.filter(content_type=comment_ct)
    
    # 4. Asignar permisos al grupo
    for perm in pizza_permissions:
        restricted_group.permissions.add(perm)
    for perm in comment_permissions:
        restricted_group.permissions.add(perm)
    
    try:
        # 5. Configurar el usuario ggavi
        admin_user = User.objects.get(username='ggavi')
        admin_user.is_staff = True  # Necesario para acceder al admin
        admin_user.groups.add(restricted_group)
        admin_user.save()
        
        print(f"Usuario {admin_user.username} configurado correctamente")
        print("\nPermisos asignados:")
        for perm in restricted_group.permissions.all():
            print(f"- {perm.codename}")
            
    except User.DoesNotExist:
        print("Error: No se encontró el usuario ggavi")

if __name__ == '__main__':
    setup_admin_user()
