from django.db import models
from decimal import Decimal


class Category(models.Model):
    """商品分类表（最多二级）"""
    parent_id = models.BigIntegerField(default=0, verbose_name='父分类ID', help_text='0表示顶级分类')
    name = models.CharField(max_length=100, verbose_name='分类名称')
    image_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='分类图片')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_show = models.IntegerField(default=1, verbose_name='是否显示', help_text='1-显示, 0-隐藏')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'categories'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
        indexes = [
            models.Index(fields=['parent_id']),
            models.Index(fields=['is_show']),
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    """商品表"""
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='分类')
    name = models.CharField(max_length=200, verbose_name='商品名称')
    subtitle = models.CharField(max_length=255, null=True, blank=True, verbose_name='商品副标题')
    main_image_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='主图URL')
    detail = models.TextField(null=True, blank=True, verbose_name='商品详情')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='原价')
    stock = models.IntegerField(default=0, verbose_name='库存')
    sales_count = models.IntegerField(default=0, verbose_name='销量')
    view_count = models.IntegerField(default=0, verbose_name='浏览量')
    status = models.IntegerField(default=1, verbose_name='状态', help_text='1-上架, 0-下架')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'products'
        verbose_name = '商品'
        verbose_name_plural = '商品'
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """商品图片表"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='商品')
    image_url = models.CharField(max_length=255, verbose_name='图片URL')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'product_images'
        verbose_name = '商品图片'
        verbose_name_plural = '商品图片'
        indexes = [
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.product.name} - 图片"
