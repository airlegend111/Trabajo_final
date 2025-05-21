from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product(models.Model):
    """
    Model representing a product in the catalog.
    """
    name = models.CharField(max_length=255, verbose_name="Nombre del producto")
    description = models.TextField(verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Imagen")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['name']

    def __str__(self):
        return self.name

class Pizza(models.Model):
    """
    Model representing a pizza in the catalog.
    """
    name = models.CharField(max_length=255, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    size = models.CharField(max_length=50, verbose_name="Tamaño")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    image = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL de la Imagen")
    
    # Campos de auditoría
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='pizzas_created',
        verbose_name="Creado por"
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='pizzas_modified',
        verbose_name="Modificado por"
    )
    created_at = models.DateTimeField(
        verbose_name="Fecha de creación",
        default=timezone.now
    )
    modified_at = models.DateTimeField(
        verbose_name="Última modificación",
        default=timezone.now
    )

    class Meta:
        verbose_name = "Pizza"
        verbose_name_plural = "Pizzas"
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} - {self.size}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es una nueva pizza
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)

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