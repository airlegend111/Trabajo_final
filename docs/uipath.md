# Automatización con UIPath para CRUD de Pizzas

## Identificadores para automatización

### Login
- URL: `/admin/login/`
- Campo usuario: `id="id_username"`
- Campo contraseña: `id="id_password"`
- Botón login: `type="submit"`

### Lista de Pizzas (Menú)
- Formulario de búsqueda: `id="pizza-search-form"`
- Campo de búsqueda: `id="pizza-search"`
- Botón buscar: `id="pizza-search-btn"`
- Filtro de tamaño: `id="pizza-size-filter"`
- Ordenamiento: `id="pizza-sort-filter"`
- Contenedor de pizzas: `id="pizza-list"`
- Cards de pizzas: `id="pizza-{id}"` (donde {id} es el ID de la pizza)
  - Imagen: `id="pizza-img-{id}"`
  - Nombre: `id="pizza-name-{id}"`
  - Descripción: `id="pizza-desc-{id}"`
  - Precio: `id="pizza-price-{id}"`
  - Botón añadir: `id="add-to-cart-{id}"`

### Carrito de Compras
- Contenedor principal: `id="cart-container"`
- Tabla de items: `id="cart-table"`
- Items del carrito: `id="cart-item-{id}"`
  - Imagen: `id="cart-img-{id}"`
  - Nombre: `id="cart-name-{id}"`
  - Tamaño: `id="cart-size-{id}"`
  - Precio: `id="cart-price-{id}"`
  - Cantidad: `id="quantity-{id}"`
  - Subtotal: `id="subtotal-{id}"`
  - Botones de cantidad: `id="increase-{id}"`, `id="decrease-{id}"`
  - Botón eliminar: `id="remove-{id}"`
- Total del carrito: `id="cart-total"`
- Botón checkout: `id="proceed-checkout"`

### Formulario de Checkout
- Contenedor: `id="checkout-container"`
- Formulario: `id="checkout-form"`
- Campos personales:
  - Nombre: `id="checkout-first-name"`
  - Apellido: `id="checkout-last-name"`
  - Dirección: `id="checkout-address"`
  - Teléfono: `id="checkout-phone"`
  - Email: `id="checkout-email"`
  - Notas: `id="checkout-notes"`
- Método de pago:
  - Efectivo: `id="payment-cash"`
  - Tarjeta: `id="payment-card"`
- Detalles de tarjeta:
  - Número: `id="card-number"`
  - Expiración: `id="card-expiry"`
  - CVV: `id="card-cvv"`
- Botón confirmar: `id="confirm-order"`
- Resumen del pedido:
  - Items: `id="order-items"`
  - Subtotal: `id="order-subtotal"`
  - Envío: `id="order-shipping"`
  - Total: `id="order-total"`

### Confirmación de Orden
- Contenedor: `id="confirmation-container"`
- Número de orden: `id="confirmation-number"`
- Fecha: `id="confirmation-date"`
- Total: `id="confirmation-total"`
- Email enviado a: `id="confirmation-email"`
- Botón volver al menú: `id="back-to-menu"`

### Lista de Pizzas (Admin)
- URL: `/admin/products/pizza/`
- Tabla de pizzas: `id="result_list"`
- Botón añadir: `class="addlink"`
- Búsqueda: `id="searchbar"`

### Formulario de Pizza
- URL: `/admin/products/pizza/add/` (nueva)
- URL: `/admin/products/pizza/{id}/change/` (editar)
- Campos del formulario:
  ```html
  <input id="id_name" name="name" type="text">
  <textarea id="id_description" name="description">
  <select id="id_size" name="size">
  <input id="id_price" name="price" type="number">
  <input id="id_image" name="image" type="url">
  ```
- Botón guardar: `name="_save"`
- Botón eliminar: `class="deletelink"`

## Secuencias de Automatización

### 1. Login Administrador
```uipath
SEQUENCE LoginAdmin
    # Abrir navegador en página de login
    OpenBrowser "http://127.0.0.1:8000/admin/"
    
    # Ingresar credenciales
    TypeInto "id_username", "ggavi"
    TypeInto "id_password", "contraseña"
    
    # Click en botón login
    Click "type=submit"
    
    # Esperar redirección
    WaitElement "/admin/"
END SEQUENCE
```

### 2. Crear Pizza
```uipath
SEQUENCE CrearPizza
    # Llamar secuencia de login
    CallSequence LoginAdmin
    
    # Ir a formulario de nueva pizza
    Click "class=addlink"
    
    # Llenar formulario
    TypeInto "id_name", pizza.Nombre
    TypeInto "id_description", pizza.Descripcion
    SelectDropdown "id_size", pizza.Tamaño
    TypeInto "id_price", pizza.Precio
    TypeInto "id_image", pizza.ImagenURL
    
    # Guardar
    Click "name=_save"
    
    # Verificar mensaje de éxito
    WaitElement "class=success"
END SEQUENCE
```

### 3. Editar Pizza
```uipath
SEQUENCE EditarPizza
    # Llamar secuencia de login
    CallSequence LoginAdmin
    
    # Buscar pizza
    TypeInto "searchbar", pizza.Nombre
    PressKey Enter
    
    # Click en pizza a editar
    Click "xpath=//td[contains(text(),'" + pizza.Nombre + "')]"
    
    # Modificar campos
    ClearField "id_price"
    TypeInto "id_price", pizza.NuevoPrecio
    
    # Guardar cambios
    Click "name=_save"
END SEQUENCE
```

### 4. Eliminar Pizza
```uipath
SEQUENCE EliminarPizza
    # Llamar secuencia de login
    CallSequence LoginAdmin
    
    # Buscar pizza
    TypeInto "searchbar", pizza.Nombre
    PressKey Enter
    
    # Click en pizza a eliminar
    Click "xpath=//td[contains(text(),'" + pizza.Nombre + "')]"
    
    # Click en botón eliminar
    Click "class=deletelink"
    
    # Confirmar eliminación
    Click "type=submit"
END SEQUENCE
```

## Variables y Configuración

```json
{
  "Config": {
    "BaseUrl": "http://127.0.0.1:8000",
    "AdminUsername": "ggavi",
    "AdminPassword": "contraseña",
    "TimeoutSeconds": 10
  },
  "Pizza": {
    "Nombre": "Pizza Test",
    "Descripcion": "Pizza para pruebas de automatización",
    "Tamaño": "Grande",
    "Precio": "15.99",
    "ImagenURL": "https://ejemplo.com/pizza.jpg"
  }
}
```

## Validaciones

Cada secuencia debe incluir las siguientes validaciones:

1. **Pre-ejecución**:
   - Verificar que el servidor esté activo
   - Validar conexión a internet
   - Comprobar credenciales

2. **Durante la ejecución**:
   - Validar campos requeridos
   - Verificar formato de datos
   - Comprobar tiempos de respuesta

3. **Post-ejecución**:
   - Verificar mensaje de éxito
   - Validar cambios en base de datos
   - Comprobar logs de operación

## Manejo de Errores

```uipath
TRY
    # Ejecutar secuencia
CATCH SystemException
    # Registrar error
    LogMessage "Error: " + SystemException.Message
    # Tomar screenshot
    TakeScreenshot
    # Reintentar o terminar
FINALLY
    # Cerrar navegador
    CloseBrowser
END TRY
```