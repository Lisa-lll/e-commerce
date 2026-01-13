"""
JWT 认证中间件（简化版）
"""
import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from users.models import User


class JWTAuthenticationMiddleware:
    """JWT 认证中间件"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # 从请求头获取 Token
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # 验证 Token
                payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
                user_id = payload.get('user_id')
                
                try:
                    user = User.objects.get(id=user_id, status=1)
                    request.user = user
                except User.DoesNotExist:
                    request.user = AnonymousUser()
            except jwt.ExpiredSignatureError:
                request.user = AnonymousUser()
            except jwt.InvalidTokenError:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
        
        response = self.get_response(request)
        return response
