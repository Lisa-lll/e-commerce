"""
工具函数
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """自定义异常处理器"""
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'code': response.status_code,
            'message': str(exc),
            'data': None,
            'timestamp': None
        }
        response.data = custom_response_data
    else:
        # 处理未捕获的异常
        custom_response_data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': '服务器内部错误',
            'data': None,
            'timestamp': None
        }
        response = Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
