from rest_framework import serializers
from .models import Order, OrderItem, CartItem
from products.serializers import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """订单商品明细序列化器"""
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_name', 'product_image', 
                  'price', 'quantity', 'total_amount', 'created_at']
        read_only_fields = ['created_at']


class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_no', 'user_id', 'status', 'status_display', 
                  'total_amount', 'freight_amount', 'pay_amount',
                  'receiver_name', 'receiver_phone', 'receiver_address', 
                  'remark', 'items', 'created_at', 'updated_at']
        read_only_fields = ['order_no', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.Serializer):
    """订单创建序列化器（支持未登录用户）"""
    # 收货信息
    receiver_name = serializers.CharField(max_length=50, required=True)
    receiver_phone = serializers.CharField(max_length=20, required=True)
    receiver_address = serializers.CharField(max_length=500, required=True)
    remark = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    # 订单商品（商品ID和数量）
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        ),
        required=True
    )
    
    def validate_items(self, value):
        """验证订单商品"""
        if not value:
            raise serializers.ValidationError("订单商品不能为空")
        
        for item in value:
            if 'product_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("订单商品格式错误")
            if item['quantity'] <= 0:
                raise serializers.ValidationError("商品数量必须大于0")
        
        return value


class CartItemSerializer(serializers.ModelSerializer):
    """购物车序列化器"""
    product = ProductListSerializer(read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
