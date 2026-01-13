from django.contrib import admin
from .models import User, UserAddress


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'nickname', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['username', 'nickname']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'receiver_name', 'receiver_phone', 'is_default']
    list_filter = ['is_default', 'created_at']
    search_fields = ['receiver_name', 'receiver_phone']
