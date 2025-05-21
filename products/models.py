from django.db import models

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

    class Meta:
        verbose_name = "Pizza"
        verbose_name_plural = "Pizzas"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.size}"