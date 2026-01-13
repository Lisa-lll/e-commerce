from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.conf import settings
import os
from datetime import datetime
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent_id', 'is_show', 'sort_order']
    list_filter = ['is_show', 'parent_id']
    search_fields = ['name']


class ProductImageForm(forms.ModelForm):
    """商品图片表单（支持文件上传）"""
    image_file = forms.ImageField(
        required=False,
        label='上传图片',
        help_text='支持格式：jpg, jpeg, png, gif, webp，最大5MB',
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )
    
    class Meta:
        model = ProductImage
        fields = ['image_file', 'image_url', 'sort_order']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 如果已有图片URL，显示提示
        if self.instance and self.instance.image_url:
            self.fields['image_url'].help_text = f'当前图片: {self.instance.image_url}'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get('image_file')
        
        if image_file:
            # 获取商品对象
            if instance.product_id:
                product = instance.product
            elif hasattr(self, 'product') and self.product:
                product = self.product
                instance.product = product
            else:
                # 如果还没有商品，先保存实例获取product（这种情况在inline中不应该发生）
                if commit:
                    instance.save()
                    if instance.product_id:
                        product = instance.product
                    else:
                        return instance
                else:
                    return instance
            
            # 验证文件大小（最大5MB）
            if image_file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('图片文件大小不能超过5MB')
            
            # 创建上传目录
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'products', str(product.id))
            os.makedirs(upload_dir, exist_ok=True)
            
            # 生成文件名
            file_ext = os.path.splitext(image_file.name)[1].lower()
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{instance.sort_order or 0}{file_ext}"
            file_path = os.path.join(upload_dir, filename)
            
            # 保存文件
            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            # 生成URL
            instance.image_url = f"{settings.MEDIA_URL}products/{product.id}/{filename}"
            
            # 如果是第一张图片，设置为商品主图
            if not product.main_image_url:
                product.main_image_url = instance.image_url
                product.save(update_fields=['main_image_url'])
        
        if commit:
            instance.save()
        return instance


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    form = ProductImageForm
    extra = 1
    fields = ['image_file', 'image_url', 'sort_order', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        """图片预览"""
        if obj and obj.image_url:
            full_url = f"{settings.MEDIA_URL.rstrip('/')}{obj.image_url}" if not obj.image_url.startswith('http') else obj.image_url
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                full_url
            )
        return "无图片"
    image_preview.short_description = '图片预览'


class ProductAdminForm(forms.ModelForm):
    """商品管理表单（支持主图上传）"""
    main_image_file = forms.ImageField(
        required=False,
        label='📷 上传主图（点击选择文件）',
        help_text='支持格式：jpg, jpeg, png, gif, webp，最大5MB。点击"选择文件"按钮上传图片。',
        widget=forms.FileInput(attrs={'accept': 'image/*', 'style': 'font-size: 14px;'})
    )
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 确保 main_image_file 字段在表单中
        if 'main_image_file' not in self.fields:
            self.fields['main_image_file'] = forms.ImageField(
                required=False,
                label='📷 上传主图（点击选择文件）',
                help_text='支持格式：jpg, jpeg, png, gif, webp，最大5MB。',
                widget=forms.FileInput(attrs={'accept': 'image/*'})
            )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['id', 'name', 'category', 'price', 'stock', 'status', 'sales_count', 'main_image_preview']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['name', 'subtitle']
    inlines = [ProductImageInline]
    readonly_fields = ['sales_count', 'view_count', 'created_at', 'updated_at', 'main_image_preview']
    
    def get_fieldsets(self, request, obj=None):
        """动态设置字段集，确保图片上传字段显示"""
        fieldsets = (
            ('基本信息', {
                'fields': ('category', 'name', 'subtitle', 'detail')
            }),
            ('价格和库存', {
                'fields': ('price', 'original_price', 'stock', 'status', 'sort_order')
            }),
            ('📷 图片上传（重要）', {
                'fields': ('main_image_file',),
                'description': '<div style="background: #f0f7ff; padding: 12px; border-left: 4px solid #1890ff; margin: 10px 0; border-radius: 4px;"><strong style="color: #1890ff; font-size: 14px;">请在此处上传商品主图</strong><br><span style="color: #666; font-size: 12px;">支持格式：jpg, jpeg, png, gif, webp<br>最大文件大小：5MB</span></div>'
            }),
            ('图片信息', {
                'fields': ('main_image_url', 'main_image_preview'),
                'classes': ('collapse',) if obj else ()
            }),
            ('统计信息', {
                'fields': ('sales_count', 'view_count', 'created_at', 'updated_at'),
                'classes': ('collapse',)
            }),
        )
        return fieldsets
    
    def main_image_preview(self, obj):
        """主图预览"""
        if obj and obj.main_image_url:
            full_url = f"{settings.MEDIA_URL.rstrip('/')}{obj.main_image_url}" if not obj.main_image_url.startswith('http') else obj.main_image_url
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                full_url
            )
        return "无主图"
    main_image_preview.short_description = '主图预览'
    
    def save_model(self, request, obj, form, change):
        """保存商品时处理主图上传"""
        # 先保存商品以获取ID（如果是新建）
        super().save_model(request, obj, form, change)
        
        # 如果上传了主图文件，处理保存
        main_image_file = form.cleaned_data.get('main_image_file')
        if main_image_file:
            # 验证文件大小
            if main_image_file.size > 5 * 1024 * 1024:
                from django.contrib import messages
                messages.error(request, '图片文件大小不能超过5MB')
                return
            
            # 创建上传目录
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'products', str(obj.id))
            os.makedirs(upload_dir, exist_ok=True)
            
            # 生成文件名
            file_ext = os.path.splitext(main_image_file.name)[1].lower()
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_main{file_ext}"
            file_path = os.path.join(upload_dir, filename)
            
            # 保存文件
            with open(file_path, 'wb+') as destination:
                for chunk in main_image_file.chunks():
                    destination.write(chunk)
            
            # 生成URL并更新
            obj.main_image_url = f"{settings.MEDIA_URL}products/{obj.id}/{filename}"
            obj.save(update_fields=['main_image_url'])
            
            # 创建ProductImage记录（如果不存在）
            if not ProductImage.objects.filter(product=obj, image_url=obj.main_image_url).exists():
                ProductImage.objects.create(
                    product=obj,
                    image_url=obj.main_image_url,
                    sort_order=0
                )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    form = ProductImageForm
    list_display = ['id', 'product', 'image_preview', 'sort_order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        """图片预览"""
        if obj and obj.image_url:
            full_url = f"{settings.MEDIA_URL.rstrip('/')}{obj.image_url}" if not obj.image_url.startswith('http') else obj.image_url
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                full_url
            )
        return "无图片"
    image_preview.short_description = '图片预览'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('product', 'image_file', 'image_url', 'sort_order', 'image_preview')
        }),
    )
