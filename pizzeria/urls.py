from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('pizzas/', views.pizzas, name='pizzas'),
    path('pizza/', views.pizza_list, name='pizza'),  # Vista adicional, pero no la usaremos en Gestión de Pizzas
    path('pizzas/create/', views.pizza_create, name='create_pizza'),
    path('pizzas/<int:pk>/update/', views.pizza_update, name='update_pizza'),
    path('pizzas/<int:pk>/delete/', views.pizza_delete, name='delete_pizza'),
]