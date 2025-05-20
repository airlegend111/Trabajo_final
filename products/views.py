from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Pizza

def menu_view(request):
    # Obtener parámetros de búsqueda y filtros
    search_query = request.GET.get('search', '')
    size_filter = request.GET.get('size', '')
    sort_by = request.GET.get('sort', 'name')  # ordenar por nombre por defecto
    
    # Filtrar pizzas
    pizzas = Pizza.objects.all()
    
    if search_query:
        pizzas = pizzas.filter(name__icontains=search_query) | pizzas.filter(description__icontains=search_query)
    
    if size_filter:
        pizzas = pizzas.filter(size=size_filter)
    
    # Ordenar resultados
    if sort_by == 'price_asc':
        pizzas = pizzas.order_by('price')
    elif sort_by == 'price_desc':
        pizzas = pizzas.order_by('-price')
    else:
        pizzas = pizzas.order_by('name')
      # Paginación
    page_number = request.GET.get('page', 1)
    paginator = Paginator(pizzas, 15)  # 15 pizzas por página
    page_obj = paginator.get_page(page_number)
      # Obtener tamaños únicos y ordenados
    sizes = ['Grande', 'Mediana', 'Pequeña']
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'size_filter': size_filter,
        'sort_by': sort_by,
        'sizes': sizes,
    }
    
    return render(request, 'menu.html', context)