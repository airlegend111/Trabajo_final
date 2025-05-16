from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 
from django.contrib import messages 
from django.db.models import Q 
from .models import Pizza, ContactMessage 
from .forms import CustomUserCreationForm, CustomAuthenticationForm, PizzaForm, ContactMessageForm

def index(request):
    pizzas = Pizza.objects.all()
    return render(request, 'pizzeria/index.html', {'pizzas': pizzas})

def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        print("Formulario recibido:", request.POST)  # Depuración
        if form.is_valid():
            print("Formulario válido, intentando guardar...")  # Depuración
            try:
                form.save()  # Guarda los datos en la tabla contact_messages
                print("Mensaje guardado con éxito.")  # Depuración
                messages.success(request, '¡Tu mensaje ha sido enviado con éxito!')
                return redirect('index')
            except Exception as e:
                print("Error al guardar el mensaje:", str(e))  # Depuración
                messages.error(request, 'Error al enviar el mensaje. Por favor, intenta de nuevo.')
        else:
            print("Formulario no válido:", form.errors)  # Depuración
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ContactMessageForm()
    return render(request, 'pizzeria/contact.html', {'form': form})

def menu(request):
    pizzas = Pizza.objects.all()
    print(f"Se encontraron {pizzas.count()} pizzas en la página de Menú")  # Para depuración
    return render(request, 'pizzeria/menu.html', {'pizzas': pizzas})

def gallery(request):
    return render(request, 'pizzeria/gallery.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'pizzeria/register.html', {'form': form})

@login_required
def pizzas(request):
    query = request.GET.get('q', '')  # Obtener el término de búsqueda del parámetro 'q'
    if query:
        pizzas = Pizza.objects.filter(name__icontains=query)  # Búsqueda insensible a mayúsculas/minúsculas por nombre
    else:
        pizzas = Pizza.objects.all()  # Mostrar todas las pizzas si no hay búsqueda
    print(f"Se encontraron {pizzas.count()} pizzas en la página de Gestión de Pizzas")  # Para depuración
    return render(request, 'pizzeria/pizzas.html', {'pizzas': pizzas, 'query': query})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'pizzeria/login.html', {'form': form})

def user_logout(request): 
    logout(request)
    return redirect('index')

@login_required
def pizza_list(request):
    query = request.GET.get('q')
    if query:
        pizzas = Pizza.objects.filter(Q(name__icontains=query))
    else:
        pizzas = Pizza.objects.all()
    return render(request, 'pizzeria/pizza.html', {'pizzas': pizzas, 'query': query})

@login_required
def pizza_create(request): 
    if request.method == 'POST': 
        form = PizzaForm(request.POST, request.FILES) 
        if form.is_valid(): 
            form.save() 
            messages.success(request, '¡Pizza añadida con éxito!') 
            return redirect('pizzas') 
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else: 
        form = PizzaForm() 
    return render(request, 'pizzeria/create_pizza.html', {'form': form, 'title': 'Añadir Pizza'})

@login_required 
def pizza_update(request, pk): 
    pizza = get_object_or_404(Pizza, pk=pk) 
    if request.method == 'POST': 
        form = PizzaForm(request.POST, request.FILES, instance=pizza) 
        if form.is_valid(): 
            form.save() 
            messages.success(request, '¡Pizza actualizada con éxito!') 
            return redirect('pizzas') 
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else: 
        form = PizzaForm(instance=pizza) 
    return render(request, 'pizzeria/update_pizza.html', {'form': form, 'title': 'Editar Pizza', 'pizza': pizza})

@login_required 
def pizza_delete(request, pk): 
    pizza = get_object_or_404(Pizza, pk=pk) 
    if request.method == 'POST': 
        pizza.delete() 
        messages.success(request, '¡Pizza eliminada con éxito!') 
        return redirect('pizzas')  # Corregido: redirige a 'pizzas', no a 'pizza'
    return render(request, 'pizzeria/delete_pizza.html', {'pizza': pizza})