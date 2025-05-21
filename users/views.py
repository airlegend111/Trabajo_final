from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, Comment
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
import json

def register_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apodo = request.POST.get('apodo')  # Este será nuestro username
        email = request.POST.get('email')
        cedula = request.POST.get('cedula')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validaciones
        if User.objects.filter(username=apodo).exists():
            messages.error(request, 'Este apodo ya está en uso. Por favor elige otro.')
            return redirect('register')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo electrónico ya está registrado.')
            return redirect('register')
        
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('register')
            
        # Validar cédula (10 dígitos)
        if len(cedula) != 10 or not cedula.isdigit():
            messages.error(request, 'La cédula debe contener 10 dígitos numéricos.')
            return redirect('register')
            
        # Crear usuario
        user = User.objects.create_user(username=apodo, email=email, password=password)
        user.first_name = nombre  # Guardamos el nombre completo en first_name
        user.save()
        
        # Crear perfil de usuario con los campos adicionales
        profile = UserProfile.objects.create(
            user=user,
            full_name=nombre,
            cedula=cedula,
            fecha_nacimiento=fecha_nacimiento
        )
        
        # Iniciar sesión automáticamente
        login(request, user)
        messages.success(request, '¡Bienvenido/a! Tu cuenta ha sido creada exitosamente.')
        return redirect('/')
        
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Intentar autenticar primero con el nombre de usuario
        user = authenticate(username=username, password=password)
        
        # Si no funciona, intentar autenticar con el email
        if user is None:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

@require_POST
def add_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Debes iniciar sesión para comentar'})
        
    content = request.POST.get('content')
    if not content:
        return JsonResponse({'status': 'error', 'message': 'El comentario no puede estar vacío'})
        
    comment = Comment.objects.create(
        user=request.user,
        content=content
    )
    
    # Datos para LogRocket
    logrocket_data = {
        'user_id': request.user.id,
        'comment_id': comment.id,
        'content_length': len(content)
    }
    
    return JsonResponse({
        'status': 'success',
        'logrocket_data': logrocket_data
    })

def get_comments(request):
    comments = Comment.objects.all().order_by('-created_at')
    comments_data = [{
        'user': comment.user.username,
        'content': comment.content,
        'date': comment.created_at.strftime('%d/%m/%Y %H:%M')
    } for comment in comments]
    
    return JsonResponse({'comments': comments_data})

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('nombre')
        email = request.POST.get('email')
        subject = request.POST.get('asunto')
        message = request.POST.get('mensaje')
        
        # Por ahora solo mostraremos un mensaje de éxito
        messages.success(request, '¡Gracias por tu mensaje! Te contactaremos pronto.')
    
    return redirect('/#contacto')