from django.db import models
from django.contrib.auth.models import User

class UserRole(models.TextChoices):
    CLIENT = 'CLIENT', 'Cliente'
    ADMIN = 'ADMIN', 'Administrador'

class UserProfile(models.Model):
    """
    Model representing a user's profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    full_name = models.CharField(max_length=255, blank=True, verbose_name="Nombre completo")
    bio = models.TextField(blank=True, verbose_name="Biografía")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name="Foto de perfil")
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.CLIENT,
        verbose_name="Rol"
    )

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"

    def __str__(self):
        return self.user.username

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    content = models.TextField(verbose_name="Contenido")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['-created_at']  # Ordenar por fecha de creación, más recientes primero
    
    def __str__(self):
        return f'Comentario de {self.user.username} - {self.created_at.strftime("%d/%m/%Y %H:%M")}'