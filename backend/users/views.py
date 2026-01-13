from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
import jwt
from django.conf import settings
from .models import User, UserAddress
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, UserAddressSerializer


def generate_jwt_token(user):
    """生成 JWT Token"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': timezone.now() + timezone.timedelta(days=int(getattr(settings, 'JWT_EXPIRE_DAYS', 7)))
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
    return token


class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # 注册登录允许所有人访问
    
    def get_queryset(self):
        """只返回当前用户的信息"""
        user_id = self.request.user.id if hasattr(self.request, 'user') and self.request.user.is_authenticated else None
        if not user_id:
            return User.objects.none()
        return User.objects.filter(id=user_id)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """用户注册"""
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'code': 200,
            'message': '注册成功',
            'data': {
                'user_id': user.id,
                'username': user.username
            },
            'timestamp': None
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """用户登录"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(username=username, status=1)
        except User.DoesNotExist:
            return Response({
                'code': 401,
                'message': '用户名或密码错误',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.check_password(password):
            return Response({
                'code': 401,
                'message': '用户名或密码错误',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # 更新最后登录时间
        user.last_login_at = timezone.now()
        user.save(update_fields=['last_login_at'])
        
        # 生成 Token
        token = generate_jwt_token(user)
        
        return Response({
            'code': 200,
            'message': '登录成功',
            'data': {
                'token': token,
                'user': UserSerializer(user).data
            },
            'timestamp': None
        })
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """获取当前用户信息"""
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else None
        if not user:
            return Response({
                'code': 401,
                'message': '请先登录',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserSerializer(user)
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data,
            'timestamp': None
        })


class UserAddressViewSet(viewsets.ModelViewSet):
    """用户地址视图集（仅登录用户）"""
    serializer_class = UserAddressSerializer
    
    def get_queryset(self):
        """只返回当前用户的地址"""
        user_id = self.request.user.id if hasattr(self.request, 'user') and self.request.user.is_authenticated else None
        if not user_id:
            return UserAddress.objects.none()
        return UserAddress.objects.filter(user_id=user_id).order_by('-is_default', '-created_at')
    
    def perform_create(self, serializer):
        """创建地址"""
        user_id = self.request.user.id if hasattr(self.request, 'user') and self.request.user.is_authenticated else None
        if not user_id:
            raise serializers.ValidationError("请先登录")
        serializer.save(user_id=user_id)
