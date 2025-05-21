from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def customer_required(view_func):
    """
    Decorator que verifica si el usuario es un cliente regular.
    Restringe el acceso a administradores restringidos.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está en el grupo RestrictedAdmin
        if request.user.groups.filter(name='RestrictedAdmin').exists():
            messages.warning(request, 'No tienes permiso para acceder a esta sección.')
            return redirect('menu')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def restricted_admin_required(view_func):
    """
    Decorator que verifica si el usuario es un administrador restringido.
    Solo permite acceso a usuarios en el grupo RestrictedAdmin.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión primero.')
            return redirect('login')
        if not request.user.groups.filter(name='RestrictedAdmin').exists():
            messages.warning(request, 'No tienes permisos de administrador restringido.')
            return redirect('menu')
        return view_func(request, *args, **kwargs)
    return _wrapped_view