from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Model representing a user's profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    full_name = models.CharField(max_length=255, blank=True, verbose_name="Nombre completo")
    bio = models.TextField(blank=True, verbose_name="Biografía")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name="Foto de perfil")

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"

    def __str__(self):
        return self.user.username