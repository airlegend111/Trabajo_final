from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import Pizza, Cart, CartItem
import json

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pizza_id = data.get('pizza_id')
            quantity = int(data.get('quantity', 1))
            
            # Validación de datos
            if not pizza_id or quantity < 1:
                return JsonResponse({'status': 'error', 'message': 'Datos inválidos'}, status=400)
            
            # Obtener o crear el carrito
            cart, created = Cart.objects.get_or_create(user=request.user)
            pizza = get_object_or_404(Pizza, id=pizza_id)
            
            # Obtener o crear el item del carrito
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, 
                pizza=pizza,
                defaults={'quantity': quantity}
            )
            
            # Si el item ya existía, actualizar la cantidad
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return JsonResponse({
                'status': 'success', 
                'message': '¡Pizza añadida al carrito!',
                'cart_count': cart.total_items
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        items = cart.items.all()
    except Cart.DoesNotExist:
        cart = None
        items = []
    
    context = {
        'cart': cart,
        'items': items
    }
    
    return render(request, 'products/cart.html', context)

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
            
            item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            
            if quantity > 0:
                item.quantity = quantity
                item.save()
            else:
                item.delete()
            
            cart = Cart.objects.get(user=request.user)
            
            return JsonResponse({
                'status': 'success',
                'cart_count': cart.total_items,
                'item_total': float(item.total_price) if quantity > 0 else 0,
                'cart_total': float(cart.total_price)
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            item.delete()
            
            cart = Cart.objects.get(user=request.user)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Item eliminado del carrito',
                'cart_count': cart.total_items,
                'cart_total': float(cart.total_price)
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
