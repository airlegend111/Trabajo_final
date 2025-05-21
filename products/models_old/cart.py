from django.db import models
from django.contrib.auth.models import User
from .product import Pizza

class Cart(models.Model):
    """
    Model representing a shopping cart.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self):
        return f"Carrito de {self.user.username}"
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    """
    Model representing an item in a shopping cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Carrito")
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, verbose_name="Pizza")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Item del carrito"
        verbose_name_plural = "Items del carrito"
        unique_together = ('cart', 'pizza')

    def __str__(self):
        return f"{self.quantity} x {self.pizza.name}"
    
    @property
    def total_price(self):
        return self.pizza.price * self.quantity
