from .models import Cart

def cart_processor(request):
    """
    Context processor that adds cart information to the context.
    """
    context = {}
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            context['user_cart'] = cart
            context['cart_item_count'] = cart.total_items
        except Cart.DoesNotExist:
            context['cart_item_count'] = 0
    
    return context
