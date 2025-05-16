from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Pizza, ContactMessage

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Correo electrónico'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Usuario'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Contraseña'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Confirmar contraseña'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Contraseña'}))

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Nombre de la pizza'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Descripción', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Precio', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full p-2 border rounded'}),
        }
class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Tu correo'}),
            'message': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Tu mensaje', 'rows': 4}),
        }