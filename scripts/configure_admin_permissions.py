from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from products.models import Pizza
from users.models import Comment

def configure_permissions():
    # 1. Crear o obtener el grupo RestrictedAdmin
    restricted_group, _ = Group.objects.get_or_create(name='RestrictedAdmin')
    
    # 2. Obtener los content types para los modelos que queremos restringir
    pizza_ct = ContentType.objects.get_for_model(Pizza)
    comment_ct = ContentType.objects.get_for_model(Comment)
    
    # 3. Limpiar permisos existentes del grupo
    restricted_group.permissions.clear()
    
    # 4. Obtener y asignar permisos específicos
    model_permissions = {
        'Pizza': ['add', 'change', 'delete', 'view'],
        'Comment': ['add', 'change', 'delete', 'view']
    }
    
    for model_name, actions in model_permissions.items():
        ct = ContentType.objects.get(app_label='products' if model_name == 'Pizza' else 'users', 
                                   model=model_name.lower())
        for action in actions:
            codename = f'{action}_{model_name.lower()}'
            try:
                perm = Permission.objects.get(content_type=ct, codename=codename)
                restricted_group.permissions.add(perm)
            except Permission.DoesNotExist:
                print(f"Warning: Permission {codename} not found")
    
    # 5. Asignar el usuario administrador al grupo
    try:
        admin_user = User.objects.get(username='ggavi')
        admin_user.groups.add(restricted_group)
        print(f"Usuario {admin_user.username} configurado con permisos restringidos")
        
        # Mostrar permisos asignados
        print("\nPermisos asignados al grupo RestrictedAdmin:")
        for perm in restricted_group.permissions.all():
            print(f"- {perm.codename}")
            
    except User.DoesNotExist:
        print("Error: No se encontró el usuario administrador")

if __name__ == '__main__':
    configure_permissions()
