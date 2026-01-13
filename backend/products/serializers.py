from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    """商品分类序列化器"""
    
    class Meta:
        model = Category
        fields = ['id', 'parent_id', 'name', 'image_url', 'sort_order', 'is_show', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ProductImageSerializer(serializers.ModelSerializer):
    """商品图片序列化器"""
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'sort_order', 'created_at']
        read_only_fields = ['created_at']


class ProductListSerializer(serializers.ModelSerializer):
    """商品列表序列化器（简化）"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'subtitle', 'main_image_url', 'price', 'original_price', 
                  'stock', 'sales_count', 'status', 'category_id', 'category_name', 'created_at']
        read_only_fields = ['created_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    """商品详情序列化器"""
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'subtitle', 'main_image_url', 'detail', 
                  'price', 'original_price', 'stock', 'sales_count', 'view_count', 
                  'status', 'sort_order', 'images', 'created_at', 'updated_at']
        read_only_fields = ['sales_count', 'view_count', 'created_at', 'updated_at']


class ProductCreateSerializer(serializers.ModelSerializer):
    """商品创建序列化器（支持图片上传）"""
    category_id = serializers.IntegerField(write_only=True, required=True)
    
    class Meta:
        model = Product
        fields = ['category_id', 'name', 'subtitle', 'detail', 'price', 'original_price', 
                  'stock', 'status', 'sort_order']
        read_only_fields = ['sales_count', 'view_count', 'main_image_url', 'created_at', 'updated_at']
    
    def validate_category_id(self, value):
        """验证分类是否存在"""
        try:
            Category.objects.get(id=value, is_show=1)
        except Category.DoesNotExist:
            raise serializers.ValidationError("分类不存在或已隐藏")
        return value
