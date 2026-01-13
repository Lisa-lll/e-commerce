from django.contrib import admin
from .models import Admin


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'name', 'status', 'last_login_at', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['username', 'name']
    readonly_fields = ['created_at', 'updated_at']
