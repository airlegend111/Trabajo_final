from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from products.models import Pizza
from users.models import Comment

def create_restricted_admin():
    # Crear grupo para administradores restringidos
    restricted_admin_group, created = Group.objects.get_or_create(name='RestrictedAdmin')
    
    # Obtener los content types necesarios
    pizza_ct = ContentType.objects.get_for_model(Pizza)
    comment_ct = ContentType.objects.get_for_model(Comment)
    
    # Obtener permisos para Pizzas (CRUD completo)
    pizza_permissions = Permission.objects.filter(content_type=pizza_ct)
    
    # Obtener permisos para Comentarios
    comment_permissions = Permission.objects.filter(content_type=comment_ct)
    
    # Asignar permisos al grupo
    for perm in pizza_permissions:
        restricted_admin_group.permissions.add(perm)
    
    for perm in comment_permissions:
        restricted_admin_group.permissions.add(perm)
    
    # Crear usuario administrador restringido
    username = 'restricted_admin'
    email = 'restricted_admin@example.com'
    password = 'admin123456'
    
    try:
        admin_user = User.objects.get(username=username)
        print(f"El usuario {username} ya existe.")
    except User.DoesNotExist:
        admin_user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True  # Necesario para acceder al admin
        )
        print(f"Usuario {username} creado exitosamente.")
      # Añadir usuario al grupo
    admin_user.groups.add(restricted_admin_group)
    
    # Añadir superusuario existente al grupo RestrictedAdmin
    try:
        superuser = User.objects.get(username='ggavi', is_superuser=True)
        superuser.groups.add(restricted_admin_group)
        print(f"Superusuario {superuser.username} añadido al grupo RestrictedAdmin")
    except User.DoesNotExist:
        print("No se encontró el superusuario ggavi")
    
    print(f"""
    Usuario administrador restringido creado:
    Username: {username}
    Password: {password}
    
    Este usuario tiene los siguientes permisos:
    - CRUD completo para Pizzas
    - CRUD completo para Comentarios
    - No puede acceder al carrito ni checkout
    """)

if __name__ == '__main__':
    create_restricted_admin()
