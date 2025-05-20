from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('add-comment/', views.add_comment, name='add_comment'),
    path('get-comments/', views.get_comments, name='get_comments'),
]