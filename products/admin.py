from django.contrib import admin
from .models import Pizza
from django.utils.html import format_html

class RestrictedPizzaAdmin(admin.ModelAdmin):
    list_display = ('preview_image', 'name', 'size', 'price', 'created_at', 'actions_column')
    list_filter = ('size', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información de la Pizza', {
            'fields': ('name', 'description', 'size', 'price')
        }),
        ('Imagen', {
            'fields': ('image',),
            'description': 'URL de la imagen de la pizza'
        })
    )
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px;">', obj.image)
        return "Sin imagen"
    preview_image.short_description = 'Vista previa'
    
    def actions_column(self, obj):
        return format_html(
            '<a class="button" href="{}">Editar</a>&nbsp;'
            '<a class="button" style="background-color: #dc3545; color: white;" href="{}">Eliminar</a>',
            f'/admin/products/pizza/{obj.id}/change/',
            f'/admin/products/pizza/{obj.id}/delete/'
        )
    actions_column.short_description = 'Acciones'
    
    class Media:
        css = {
            'all': ('css/admin_styles.css',)
        }

class RestrictedCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'content')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content')
    
    def has_module_permission(self, request):
        return request.user.groups.filter(name='RestrictedAdmin').exists()
    
    def has_add_permission(self, request):
        return request.user.groups.filter(name='RestrictedAdmin').exists()
    
    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='RestrictedAdmin').exists()
    
    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='RestrictedAdmin').exists()
    
    def has_view_permission(self, request, obj=None):
        return request.user.groups.filter(name='RestrictedAdmin').exists()

class RestrictedCartAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

class RestrictedCartItemAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

# Registrar los modelos con las clases de administración restringida
admin.site.register(Pizza, RestrictedPizzaAdmin)
admin.site.register(Comment, RestrictedCommentAdmin)
admin.site.register(Cart, RestrictedCartAdmin)
admin.site.register(CartItem, RestrictedCartItemAdmin)