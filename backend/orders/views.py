from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.utils import timezone
import random
import string
from .models import Order, OrderItem, CartItem
from .serializers import OrderSerializer, OrderCreateSerializer, CartItemSerializer
from products.models import Product


def generate_order_no():
    """生成订单号"""
    return 'ORD' + timezone.now().strftime('%Y%m%d%H%M%S') + ''.join(random.choices(string.digits, k=4))


class OrderViewSet(viewsets.ModelViewSet):
    """订单视图集"""
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  # 允许未登录用户访问
    
    def get_queryset(self):
        """根据用户身份返回不同的查询集"""
        user_id = self.request.user.id if hasattr(self.request, 'user') and self.request.user.is_authenticated else None
        
        if user_id:
            # 登录用户：返回自己的订单
            return Order.objects.filter(user_id=user_id).order_by('-created_at')
        else:
            # 未登录用户：返回空查询集（只能通过订单号查询）
            return Order.objects.none()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """创建订单（支持未登录用户）"""
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        items_data = validated_data.pop('items')
        
        # 获取用户ID（如果已登录）
        user_id = request.user.id if hasattr(request, 'user') and request.user.is_authenticated else None
        
        # 计算订单金额
        total_amount = 0
        order_items_data = []
        
        for item in items_data:
            try:
                product = Product.objects.get(id=item['product_id'], status=1)
            except Product.DoesNotExist:
                return Response({
                    'code': 400,
                    'message': f'商品 {item["product_id"]} 不存在或已下架',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 检查库存
            if product.stock < item['quantity']:
                return Response({
                    'code': 400,
                    'message': f'商品 {product.name} 库存不足',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            item_total = product.price * item['quantity']
            total_amount += item_total
            
            order_items_data.append({
                'product': product,
                'product_name': product.name,
                'product_image': product.main_image_url,
                'price': product.price,
                'quantity': item['quantity'],
                'total_amount': item_total
            })
        
        # 计算运费（简化版：固定运费或根据金额计算）
        freight_amount = 0  # 可以后续实现运费计算逻辑
        pay_amount = total_amount + freight_amount
        
        # 创建订单
        order = Order.objects.create(
            order_no=generate_order_no(),
            user_id=user_id,
            status=1,  # 待付款
            total_amount=total_amount,
            freight_amount=freight_amount,
            pay_amount=pay_amount,
            receiver_name=validated_data['receiver_name'],
            receiver_phone=validated_data['receiver_phone'],
            receiver_address=validated_data['receiver_address'],
            remark=validated_data.get('remark', '')
        )
        
        # 创建订单商品
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                product_name=item_data['product_name'],
                product_image=item_data['product_image'],
                price=item_data['price'],
                quantity=item_data['quantity'],
                total_amount=item_data['total_amount']
            )
            
            # 减少库存
            item_data['product'].stock -= item_data['quantity']
            item_data['product'].sales_count += item_data['quantity']
            item_data['product'].save(update_fields=['stock', 'sales_count'])
        
        # 如果用户已登录，清空购物车
        if user_id:
            CartItem.objects.filter(user_id=user_id).delete()
        
        serializer = OrderSerializer(order)
        return Response({
            'code': 200,
            'message': '订单创建成功',
            'data': serializer.data,
            'timestamp': None
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def query(self, request):
        """订单查询（未登录用户通过订单号和/或手机号查询）"""
        order_no = request.data.get('order_no', '').strip()
        receiver_phone = request.data.get('receiver_phone', '').strip()
        
        # 至少填写一个
        if not order_no and not receiver_phone:
            return Response({
                'code': 400,
                'message': '请至少填写订单号或手机号',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 构建查询条件
        query_params = {}
        if order_no:
            query_params['order_no'] = order_no
        if receiver_phone:
            query_params['receiver_phone'] = receiver_phone
        
        try:
            # 根据查询条件查询订单
            orders = Order.objects.filter(**query_params).order_by('-created_at')
            
            if not orders.exists():
                return Response({
                    'code': 404,
                    'message': '未找到匹配的订单',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_404_NOT_FOUND)
            
            # 如果只查询到一个订单，返回单个订单
            if orders.count() == 1:
                serializer = OrderSerializer(orders.first())
                return Response({
                    'code': 200,
                    'message': 'success',
                    'data': serializer.data,
                    'timestamp': None
                })
            else:
                # 多个订单，返回列表
                serializer = OrderSerializer(orders, many=True)
                return Response({
                    'code': 200,
                    'message': f'找到 {orders.count()} 个订单',
                    'data': serializer.data,
                    'timestamp': None
                })
        except Exception as e:
            return Response({
                'code': 500,
                'message': f'查询失败: {str(e)}',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['patch', 'put'])
    def update_status(self, request, pk=None):
        """修改订单状态"""
        try:
            order = self.get_object()
            new_status = request.data.get('status')
            
            if new_status is None:
                return Response({
                    'code': 400,
                    'message': '请提供订单状态',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证状态值
            valid_statuses = [1, 2, 3, 4, 5]
            if new_status not in valid_statuses:
                return Response({
                    'code': 400,
                    'message': f'无效的订单状态，有效值：{valid_statuses}',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 更新订单状态
            order.status = new_status
            order.save(update_fields=['status', 'updated_at'])
            
            serializer = OrderSerializer(order)
            return Response({
                'code': 200,
                'message': '订单状态更新成功',
                'data': serializer.data,
                'timestamp': None
            })
        except Order.DoesNotExist:
            return Response({
                'code': 404,
                'message': '订单不存在',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'code': 500,
                'message': f'更新失败: {str(e)}',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartItemViewSet(viewsets.ModelViewSet):
    """购物车视图集（仅登录用户）"""
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]  # 中间件会处理认证
    
    def get_queryset(self):
        """只返回当前用户的购物车"""
        user_id = self.request.user.id if hasattr(self.request, 'user') and self.request.user.is_authenticated else None
        if not user_id:
            return CartItem.objects.none()
        return CartItem.objects.filter(user_id=user_id).order_by('-created_at')
    
    def perform_create(self, serializer):
        """创建购物车项"""
        user_id = self.request.user.id if hasattr(self.request, 'user') and self.request.user.is_authenticated else None
        if not user_id:
            raise serializers.ValidationError("请先登录")
        serializer.save(user_id=user_id)
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        """添加商品到购物车"""
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        user_id = request.user.id if hasattr(request, 'user') and request.user.is_authenticated else None
        if not user_id:
            return Response({
                'code': 401,
                'message': '请先登录',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            product = Product.objects.get(id=product_id, status=1)
        except Product.DoesNotExist:
            return Response({
                'code': 400,
                'message': '商品不存在或已下架',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查是否已存在
        cart_item, created = CartItem.objects.get_or_create(
            user_id=user_id,
            product_id=product_id,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response({
            'code': 200,
            'message': '添加成功',
            'data': serializer.data,
            'timestamp': None
        })
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """清空购物车"""
        user_id = request.user.id if hasattr(request, 'user') and request.user.is_authenticated else None
        if not user_id:
            return Response({
                'code': 401,
                'message': '请先登录',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        CartItem.objects.filter(user_id=user_id).delete()
        return Response({
            'code': 200,
            'message': '购物车已清空',
            'data': None,
            'timestamp': None
        })
