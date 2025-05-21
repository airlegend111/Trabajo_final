from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('add-comment/', views.add_comment, name='add_comment'),
    path('get-comments/', views.get_comments, name='get_comments'),
    path('contact/', views.contact_view, name='contact'),
]