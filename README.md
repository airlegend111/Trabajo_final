# Bigotes Pizzería - Sistema de Pedidos Online

## 📝 Descripción
Bigotes Pizzería es una aplicación web desarrollada con Django que permite a los usuarios explorar el menú de pizzas, realizar pedidos y gestionar su carrito de compras. La aplicación está diseñada para ofrecer una experiencia de usuario intuitiva y moderna.

## 🚀 Características

- **Gestión de Usuarios**
  - Registro e inicio de sesión de usuarios
  - Perfiles personalizados
  - Sistema de autenticación seguro

- **Catálogo de Pizzas**
  - Visualización de menú con imágenes
  - Filtros por tamaño
  - Búsqueda de pizzas
  - Ordenamiento por precio y nombre

- **Carrito de Compras**
  - Añadir/eliminar productos
  - Actualizar cantidades
  - Visualización de subtotales
  - Límite de 10 unidades por producto

- **Proceso de Checkout**
  - Formulario de entrega
  - Resumen del pedido
  - Confirmación de la orden
  - Cálculo de costos de envío

## 🛠️ Tecnologías Utilizadas

- **Backend**
  - Python 3.12+
  - Django 4.2
  - SQLite3

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap 5.3
  - Font Awesome
  - jQuery

## 📦 Estructura del Proyecto

```
├── myproject/          # Configuración principal del proyecto
├── products/          # Aplicación de productos y carrito
├── users/            # Aplicación de gestión de usuarios
├── static/           # Archivos estáticos (CSS, JS, imágenes)
├── templates/        # Plantillas HTML
├── docs/            # Documentación
├── scripts/         # Scripts de utilidad
└── manage.py        # Script de gestión de Django
```

## 🚀 Instalación y Configuración

1. Clonar el repositorio:
   ```bash
   git clone [url-del-repositorio]
   ```

2. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\\Scripts\\activate  # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Realizar migraciones:
   ```bash
   python manage.py migrate
   ```

5. Cargar datos iniciales:
   ```bash
   python manage.py loaddata initial_data.json
   ```

6. Iniciar el servidor:
   ```bash
   python manage.py runserver
   ```

## 🌐 Uso de la Aplicación

1. **Registro/Login**
   - Crear una cuenta nueva o iniciar sesión
   - Acceder a funcionalidades personalizadas

2. **Explorar el Menú**
   - Ver catálogo de pizzas
   - Usar filtros y búsqueda
   - Ver detalles de productos

3. **Gestionar Carrito**
   - Añadir pizzas al carrito
   - Ajustar cantidades
   - Eliminar productos

4. **Realizar Pedido**
   - Completar información de entrega
   - Revisar resumen del pedido
   - Confirmar y finalizar compra

## 👥 Equipo de Desarrollo

- Backend Developer: Gabriela Vilchez

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 📱 Principales Funcionalidades

1. **Gestión de Usuarios**
   - Sistema de autenticación seguro
   - Registro de nuevos usuarios
   - Login/Logout
   - Perfiles personalizados

2. **Catálogo de Productos**
   - Listado de pizzas con imágenes
   - Filtros por tamaño
   - Búsqueda por nombre o descripción
   - Ordenamiento por precio y nombre

3. **Carrito de Compras**
   - Añadir/eliminar productos
   - Actualizar cantidades
   - Vista previa del pedido
   - Cálculo automático de subtotales

4. **Proceso de Compra**
   - Checkout seguro
   - Formulario de entrega
   - Confirmación del pedido
   - Resumen de la compra

## 🤝 Contribución

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crear una nueva rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit los cambios (`git commit -am 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear un Pull Request

## 📞 Soporte

Para soporte técnico o preguntas:
- Email: [geronimo.gaviria@upb.edu.co]
- GitHub Issues: [Crear un issue en el repositorio]