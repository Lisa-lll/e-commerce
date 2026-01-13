from django.contrib import admin
from .models import Order, OrderItem, CartItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_image', 'price', 'total_amount']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_no', 'user', 'status', 'pay_amount', 'receiver_name', 'receiver_phone', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_no', 'receiver_name', 'receiver_phone']
    readonly_fields = ['order_no', 'created_at', 'updated_at']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product_name', 'quantity', 'price', 'total_amount']
    list_filter = ['created_at']
    search_fields = ['product_name']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']
