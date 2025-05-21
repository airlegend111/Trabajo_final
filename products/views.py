from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
import json
import time
import datetime
from .models import Pizza, Cart, CartItem

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pizza_id = data.get('pizza_id')
            quantity = int(data.get('quantity', 1))
            
            # Validación de datos
            if not pizza_id:
                return JsonResponse({'status': 'error', 'message': 'ID de pizza no proporcionado'}, status=400)
            
            if quantity < 1 or quantity > 10:
                return JsonResponse({'status': 'error', 'message': 'La cantidad debe estar entre 1 y 10'}, status=400)
            
            # Verificar si la pizza existe
            try:
                pizza = Pizza.objects.get(id=pizza_id)
            except Pizza.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'La pizza seleccionada no existe'}, status=404)
            
            # Obtener o crear el carrito
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Obtener o crear el item del carrito
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, 
                pizza=pizza,
                defaults={'quantity': quantity}
            )
            
            # Si el item ya existía, actualizar la cantidad
            if not created:
                # Validar que no exceda el límite
                new_quantity = cart_item.quantity + quantity
                if new_quantity > 10:
                    return JsonResponse({
                        'status': 'error', 
                        'message': 'No puedes añadir más de 10 unidades del mismo producto'
                    }, status=400)
                
                cart_item.quantity = new_quantity
                cart_item.save()
            
            return JsonResponse({
                'status': 'success', 
                'message': '¡Pizza añadida al carrito!',
                'cart_count': cart.total_items,
                'item_name': pizza.name,
                'item_quantity': cart_item.quantity
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Formato JSON inválido'}, status=400)
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': f'Error de valor: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@login_required
def view_cart(request):
    try:
        # Intentar obtener el carrito del usuario
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all().select_related('pizza')  # Optimizar consulta con select_related
        
        context = {
            'cart': cart,
            'items': items,
            'cart_count': cart.total_items,
            'cart_total': cart.total_price
        }
        
    except Exception as e:
        # En caso de error, mostrar un carrito vacío con mensaje de error
        context = {
            'error_message': f"Error al cargar el carrito: {str(e)}",
            'cart': None,
            'items': [],
            'cart_count': 0,
            'cart_total': 0
        }
    
    return render(request, 'products/cart.html', context)

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
            
            # Validar la cantidad
            if quantity < 1 or quantity > 10:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'La cantidad debe estar entre 1 y 10'
                }, status=400)
            
            # Verificar que el item exista y pertenezca al usuario actual
            try:
                item = CartItem.objects.get(id=item_id, cart__user=request.user)
            except CartItem.DoesNotExist:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'El item no existe en tu carrito'
                }, status=404)
            
            # Actualizar la cantidad
            item.quantity = quantity
            item.save()
            
            # Obtener el carrito actualizado
            cart = Cart.objects.get(user=request.user)
            
            return JsonResponse({
                'status': 'success',
                'cart_count': cart.total_items,
                'item_total': float(item.total_price),
                'cart_total': float(cart.total_price),
                'item_name': item.pizza.name
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Formato JSON inválido'}, status=400)
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': f'Error de valor: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            # Verificar que el item exista y pertenezca al usuario actual
            try:
                item = CartItem.objects.get(id=item_id, cart__user=request.user)
            except CartItem.DoesNotExist:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'El item no existe en tu carrito'
                }, status=404)
            
            # Guardar información del item antes de eliminarlo
            item_name = item.pizza.name
            
            # Eliminar el item
            item.delete()
            
            # Obtener el carrito actualizado
            cart = Cart.objects.get(user=request.user)
            
            return JsonResponse({
                'status': 'success',
                'message': f'{item_name} eliminado del carrito',
                'cart_count': cart.total_items,
                'cart_total': float(cart.total_price)
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

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

@login_required
def checkout(request):
    try:
        # Verificar que el usuario tenga un carrito con items
        try:
            cart = Cart.objects.get(user=request.user)
            if cart.total_items == 0:
                messages.warning(request, "Tu carrito está vacío. Añade algunos productos antes de proceder al pago.")
                return redirect('cart')
                
            items = cart.items.all().select_related('pizza')
            shipping_cost = 2.00  # Costo fijo de envío
            total_with_shipping = float(cart.total_price) + shipping_cost
            
        except Cart.DoesNotExist:
            messages.error(request, "No se encontró tu carrito. Por favor, intenta nuevamente.")
            return redirect('menu')
        
        # Procesar el formulario cuando se envía
        if request.method == 'POST':
            # Aquí se procesaría el formulario de pago
            # Por ahora, solo redireccionamos a la confirmación
            
            # Generamos un número de pedido único
            order_number = f"{request.user.id}-{int(time.time())}"
            
            # Guardar la información de la orden en la sesión para la página de confirmación
            request.session['order_info'] = {
                'number': order_number,
                'date': datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),
                'total': total_with_shipping,
                'items': [{'name': item.pizza.name, 'quantity': item.quantity, 'price': float(item.total_price)} for item in items]
            }
            
            # En un caso real, aquí se guardaría la orden en la base de datos
            
            # Limpiar el carrito
            cart.items.all().delete()
            
            return redirect('order_confirmation')
        
        context = {
            'cart': cart,
            'items': items,
            'total_with_shipping': total_with_shipping
        }
        
        return render(request, 'products/checkout.html', context)
        
    except Exception as e:
        messages.error(request, f"Error al procesar el checkout: {str(e)}")
        return redirect('cart')

@login_required
def order_confirmation(request):
    # Recuperar información de la orden desde la sesión
    order_info = request.session.get('order_info', {})
    
    if not order_info:
        messages.error(request, "No se encontró información del pedido. Por favor, realiza un nuevo pedido.")
        return redirect('menu')
    
    context = {
        'order_number': order_info.get('number', 'N/A'),
        'order_date': order_info.get('date', datetime.datetime.now().strftime('%d/%m/%Y %H:%M')),
        'order_total': order_info.get('total', 0),
        'order_items': order_info.get('items', [])
    }
    
    # Eliminar la información de la sesión para evitar duplicados
    if 'order_info' in request.session:
        del request.session['order_info']
    
    return render(request, 'products/order_confirmation.html', context)