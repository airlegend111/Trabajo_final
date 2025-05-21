from django.contrib import admin
from .models import UserProfile, Comment

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'full_name')

admin.site.register(Comment)