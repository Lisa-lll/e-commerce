from django.db import models
from users.models import User
from products.models import Product
from decimal import Decimal


class Order(models.Model):
    """订单表（支持未登录用户，user_id 可为空）"""
    ORDER_STATUS_CHOICES = [
        (1, '待付款'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '已完成'),
        (5, '已取消'),
    ]

    order_no = models.CharField(max_length=32, unique=True, verbose_name='订单号')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name='用户')
    status = models.IntegerField(default=1, choices=ORDER_STATUS_CHOICES, verbose_name='订单状态')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总金额')
    freight_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='运费')
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='实付金额')
    receiver_name = models.CharField(max_length=50, verbose_name='收货人')
    receiver_phone = models.CharField(max_length=20, verbose_name='收货电话')
    receiver_address = models.CharField(max_length=500, verbose_name='收货地址')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='订单备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'orders'
        verbose_name = '订单'
        verbose_name_plural = '订单'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['order_no']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['receiver_phone']),  # 用于未登录用户查询订单
        ]

    def __str__(self):
        return f"订单 {self.order_no}"


class OrderItem(models.Model):
    """订单商品明细表"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='商品')
    product_name = models.CharField(max_length=200, verbose_name='商品名称（快照）')
    product_image = models.CharField(max_length=255, null=True, blank=True, verbose_name='商品图片（快照）')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价（快照）')
    quantity = models.IntegerField(verbose_name='数量')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='小计')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'order_items'
        verbose_name = '订单商品'
        verbose_name_plural = '订单商品'
        indexes = [
            models.Index(fields=['order']),
        ]

    def __str__(self):
        return f"{self.order.order_no} - {self.product_name}"


class CartItem(models.Model):
    """购物车表（仅登录用户）"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cartItems', verbose_name='用户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartItems', verbose_name='商品')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'cart_items'
        verbose_name = '购物车'
        verbose_name_plural = '购物车'
        unique_together = [['user', 'product']]
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
