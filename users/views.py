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
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return redirect('register')
            
        user = User.objects.create_user(username=username, password=password, email=email)
        UserProfile.objects.create(user=user)
        
        login(request, user)
        return redirect('/')
        
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
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