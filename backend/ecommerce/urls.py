"""
URL configuration for ecommerce project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

# 设置 Django Admin 站点名称
admin.site.site_header = '黄石小店管理后台'
admin.site.site_title = '黄石小店'
admin.site.index_title = '欢迎使用黄石小店管理后台'

@api_view(['GET'])
def health_check(request):
    """健康检查"""
    return Response({
        'code': 200,
        'message': '服务运行正常',
        'timestamp': request.timestamp if hasattr(request, 'timestamp') else None
    })

@api_view(['GET'])
def api_info(request):
    """API 信息"""
    return Response({
        'code': 200,
        'message': 'API 服务正常',
        'version': '1.0.0',
        'timestamp': request.timestamp if hasattr(request, 'timestamp') else None
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', health_check, name='health'),
    path('api/v1/', api_info, name='api-info'),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('products.urls')),
    path('api/v1/', include('orders.urls')),
    # path('api/v1/admin/', include('admins.urls')),  # 管理后台 API 后续添加
]

# 开发环境：提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
