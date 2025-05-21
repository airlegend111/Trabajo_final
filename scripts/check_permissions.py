from django.contrib.auth.models import Group, User

# Verificar grupo
group = Group.objects.get(name='RestrictedAdmin')
print(f'Grupo encontrado: {group.name}')

# Verificar usuario
user = User.objects.get(username='ggavi')
print(f'Usuario en grupo RestrictedAdmin: {user.groups.filter(name="RestrictedAdmin").exists()}')

# Mostrar permisos
print('\nPermisos del grupo:')
for perm in group.permissions.all():
    print(f'- {perm.codename}')
