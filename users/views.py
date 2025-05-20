from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Comment
from django.urls import reverse

def get_logrocket_context(request):
    context = {}
    if request.user.is_authenticated:
        context['logrocket_user'] = {
            'id': str(request.user.id),  # Convertir a string para seguridad
            'name': request.user.username,
            'email': request.user.email,
            'isStaff': request.user.is_staff,
            'dateJoined': request.user.date_joined.isoformat(),
            'lastLogin': request.user.last_login.isoformat() if request.user.last_login else None,
        }
    return context

def login_view(request):
    context = get_logrocket_context(request)
    return render(request, 'login.html', context)

def register_view(request):
    context = get_logrocket_context(request)
    return render(request, 'register.html', context)

@login_required
def add_comment(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(
                user=request.user,
                content=content
            )
            # Registrar evento en LogRocket con más detalles
            logrocket_data = {
                'user_id': str(request.user.id),
                'comment_id': str(comment.id),
                'content_length': len(content),
                'user_name': request.user.username,
                'timestamp': comment.created_at.isoformat(),
                'is_staff': request.user.is_staff
            }
            return JsonResponse({
                'status': 'success',
                'logrocket_data': logrocket_data
            })
    return JsonResponse({'status': 'error'})

def get_comments(request):
    comments = Comment.objects.select_related('user').all()
    return JsonResponse({
        'comments': [
            {
                'user': comment.user.username,
                'content': comment.content,
                'date': comment.created_at.strftime("%d/%m/%Y %H:%M")
            } for comment in comments
        ]
    })