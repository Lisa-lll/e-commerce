from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django.conf import settings
import os
from datetime import datetime
from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer, ProductImageSerializer, ProductCreateSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """标准分页"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """商品分类视图集（只读）"""
    queryset = Category.objects.filter(is_show=1).order_by('sort_order', 'id')
    serializer_class = CategorySerializer
    
    def list(self, request, *args, **kwargs):
        """分类列表（统一返回格式）"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data,
            'timestamp': None
        })
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取分类树（最多二级）"""
        categories = self.queryset.all()
        
        # 构建分类树
        tree = []
        parent_map = {}
        
        # 第一遍：创建所有分类的映射
        for cat in categories:
            parent_map[cat.id] = {
                'id': cat.id,
                'name': cat.name,
                'image_url': cat.image_url,
                'children': []
            }
        
        # 第二遍：构建树结构
        for cat in categories:
            if cat.parent_id == 0:
                # 顶级分类
                tree.append(parent_map[cat.id])
            else:
                # 子分类
                if cat.parent_id in parent_map:
                    parent_map[cat.parent_id]['children'].append(parent_map[cat.id])
        
        return Response({
            'code': 200,
            'message': 'success',
            'data': tree,
            'timestamp': None
        })


class ProductViewSet(viewsets.ModelViewSet):
    """商品视图集（支持创建、更新、删除）"""
    queryset = Product.objects.all().order_by('-sort_order', '-created_at')
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """根据action返回不同的查询集"""
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'search':
            # 列表和详情只显示上架商品
            return Product.objects.filter(status=1).order_by('-sort_order', '-created_at')
        # 创建、更新、删除时显示所有商品
        return Product.objects.all().order_by('-sort_order', '-created_at')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return ProductCreateSerializer
        return ProductListSerializer
    
    def get_parser_classes(self):
        """根据action返回不同的解析器"""
        if self.action == 'create' or self.action == 'upload_image':
            return [MultiPartParser, FormParser]
        return super().get_parser_classes()
    
    def create(self, request, *args, **kwargs):
        """创建商品（支持同时上传图片）"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 获取分类ID
        category_id = serializer.validated_data.pop('category_id')
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({
                'code': 400,
                'message': '分类不存在',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建商品
        product = Product.objects.create(
            category=category,
            **serializer.validated_data
        )
        
        # 处理图片上传
        uploaded_images = []
        
        # 处理主图（main_image）
        main_image = request.FILES.get('main_image')
        if main_image:
            image_url = self._save_image(product, main_image, is_main=True)
            product.main_image_url = image_url
            product.save(update_fields=['main_image_url'])
            uploaded_images.append(image_url)
        
        # 处理多张图片（images[]）
        images = request.FILES.getlist('images')
        for idx, image_file in enumerate(images):
            image_url = self._save_image(product, image_file, sort_order=idx)
            uploaded_images.append(image_url)
        
        # 如果没有上传图片但提供了main_image_url，直接使用
        if not uploaded_images and request.data.get('main_image_url'):
            product.main_image_url = request.data.get('main_image_url')
            product.save(update_fields=['main_image_url'])
        
        # 返回商品详情
        detail_serializer = ProductDetailSerializer(product)
        return Response({
            'code': 200,
            'message': '商品创建成功',
            'data': detail_serializer.data,
            'timestamp': None
        }, status=status.HTTP_201_CREATED)
    
    def _save_image(self, product, image_file, is_main=False, sort_order=0):
        """保存图片的辅助方法"""
        # 验证文件类型
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        file_ext = os.path.splitext(image_file.name)[1].lower()
        if file_ext not in allowed_extensions:
            raise serializers.ValidationError(f'不支持的图片格式，支持格式：{", ".join(allowed_extensions)}')
        
        # 验证文件大小（最大5MB）
        max_size = 5 * 1024 * 1024  # 5MB
        if image_file.size > max_size:
            raise serializers.ValidationError('图片文件大小不能超过5MB')
        
        # 创建上传目录
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'products', str(product.id))
        os.makedirs(upload_dir, exist_ok=True)
        
        # 生成文件名（使用时间戳避免重名）
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{sort_order}{file_ext}"
        file_path = os.path.join(upload_dir, filename)
        
        # 保存文件
        with open(file_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        
        # 生成URL
        image_url = f"{settings.MEDIA_URL}products/{product.id}/{filename}"
        
        # 创建商品图片记录
        ProductImage.objects.create(
            product=product,
            image_url=image_url,
            sort_order=sort_order
        )
        
        return image_url
    
    def retrieve(self, request, *args, **kwargs):
        """商品详情（增加浏览量）"""
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        
        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data,
            'timestamp': None
        })
    
    def list(self, request, *args, **kwargs):
        """商品列表"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # 分类筛选
        category_id = request.query_params.get('category_id', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # 搜索
        search = request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(subtitle__icontains=search)
            )
        
        # 价格排序
        price_order = request.query_params.get('price_order', None)
        if price_order == 'asc':
            queryset = queryset.order_by('price')
        elif price_order == 'desc':
            queryset = queryset.order_by('-price')
        
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            # 包装分页响应，统一返回格式
            return Response({
                'code': 200,
                'message': 'success',
                'data': {
                    'results': paginated_response.data.get('results', []),
                    'count': paginated_response.data.get('count', 0),
                    'next': paginated_response.data.get('next'),
                    'previous': paginated_response.data.get('previous'),
                },
                'timestamp': None
            })
        
        # 无分页时直接返回数组
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data,
            'timestamp': None
        })
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """商品搜索"""
        keyword = request.query_params.get('keyword', '')
        if not keyword:
            return Response({
                'code': 400,
                'message': '请输入搜索关键词',
                'data': [],
                'timestamp': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.queryset.filter(
            Q(name__icontains=keyword) | Q(subtitle__icontains=keyword)
        )[:20]  # 限制返回数量
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data,
            'timestamp': None
        })
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_image(self, request, pk=None):
        """上传商品图片"""
        try:
            product = self.get_object()
            image_file = request.FILES.get('image')
            
            if not image_file:
                return Response({
                    'code': 400,
                    'message': '请提供图片文件',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证文件类型
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            file_ext = os.path.splitext(image_file.name)[1].lower()
            if file_ext not in allowed_extensions:
                return Response({
                    'code': 400,
                    'message': f'不支持的图片格式，支持格式：{", ".join(allowed_extensions)}',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证文件大小（最大5MB）
            max_size = 5 * 1024 * 1024  # 5MB
            if image_file.size > max_size:
                return Response({
                    'code': 400,
                    'message': '图片文件大小不能超过5MB',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 创建上传目录
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'products', str(product.id))
            os.makedirs(upload_dir, exist_ok=True)
            
            # 生成文件名（使用时间戳避免重名）
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}{file_ext}"
            file_path = os.path.join(upload_dir, filename)
            
            # 保存文件
            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            # 生成URL
            image_url = f"{settings.MEDIA_URL}products/{product.id}/{filename}"
            
            # 获取排序顺序（默认为已有图片数量）
            sort_order = request.data.get('sort_order', product.images.count())
            
            # 创建商品图片记录
            product_image = ProductImage.objects.create(
                product=product,
                image_url=image_url,
                sort_order=sort_order
            )
            
            # 如果是第一张图片，设置为商品主图
            if not product.main_image_url:
                product.main_image_url = image_url
                product.save(update_fields=['main_image_url'])
            
            serializer = ProductImageSerializer(product_image)
            return Response({
                'code': 200,
                'message': '图片上传成功',
                'data': serializer.data,
                'timestamp': None
            }, status=status.HTTP_201_CREATED)
            
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'code': 500,
                'message': f'上传失败: {str(e)}',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['patch', 'put'])
    def set_main_image(self, request, pk=None):
        """设置商品主图"""
        try:
            product = self.get_object()
            image_id = request.data.get('image_id')
            
            if not image_id:
                return Response({
                    'code': 400,
                    'message': '请提供图片ID',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                product_image = ProductImage.objects.get(id=image_id, product=product)
                product.main_image_url = product_image.image_url
                product.save(update_fields=['main_image_url'])
                
                serializer = ProductDetailSerializer(product)
                return Response({
                    'code': 200,
                    'message': '主图设置成功',
                    'data': serializer.data,
                    'timestamp': None
                })
            except ProductImage.DoesNotExist:
                return Response({
                    'code': 404,
                    'message': '图片不存在',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'code': 500,
                'message': f'设置失败: {str(e)}',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_image(self, request, pk=None):
        """上传商品图片"""
        try:
            product = self.get_object()
            image_file = request.FILES.get('image')
            
            if not image_file:
                return Response({
                    'code': 400,
                    'message': '请提供图片文件',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证文件类型
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            file_ext = os.path.splitext(image_file.name)[1].lower()
            if file_ext not in allowed_extensions:
                return Response({
                    'code': 400,
                    'message': f'不支持的图片格式，支持格式：{", ".join(allowed_extensions)}',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证文件大小（最大5MB）
            max_size = 5 * 1024 * 1024  # 5MB
            if image_file.size > max_size:
                return Response({
                    'code': 400,
                    'message': '图片文件大小不能超过5MB',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 创建上传目录
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'products', str(product.id))
            os.makedirs(upload_dir, exist_ok=True)
            
            # 生成文件名（使用时间戳避免重名）
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}{file_ext}"
            file_path = os.path.join(upload_dir, filename)
            
            # 保存文件
            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            # 生成URL
            image_url = f"{settings.MEDIA_URL}products/{product.id}/{filename}"
            
            # 获取排序顺序（默认为已有图片数量）
            sort_order = request.data.get('sort_order', product.images.count())
            
            # 创建商品图片记录
            product_image = ProductImage.objects.create(
                product=product,
                image_url=image_url,
                sort_order=sort_order
            )
            
            # 如果是第一张图片，设置为商品主图
            if not product.main_image_url:
                product.main_image_url = image_url
                product.save(update_fields=['main_image_url'])
            
            serializer = ProductImageSerializer(product_image)
            return Response({
                'code': 200,
                'message': '图片上传成功',
                'data': serializer.data,
                'timestamp': None
            }, status=status.HTTP_201_CREATED)
            
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'code': 500,
                'message': f'上传失败: {str(e)}',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['patch', 'put'])
    def set_main_image(self, request, pk=None):
        """设置商品主图"""
        try:
            product = self.get_object()
            image_id = request.data.get('image_id')
            
            if not image_id:
                return Response({
                    'code': 400,
                    'message': '请提供图片ID',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                product_image = ProductImage.objects.get(id=image_id, product=product)
                product.main_image_url = product_image.image_url
                product.save(update_fields=['main_image_url'])
                
                serializer = ProductDetailSerializer(product)
                return Response({
                    'code': 200,
                    'message': '主图设置成功',
                    'data': serializer.data,
                    'timestamp': None
                })
            except ProductImage.DoesNotExist:
                return Response({
                    'code': 404,
                    'message': '图片不存在',
                    'data': None,
                    'timestamp': None
                }, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({
                'code': 404,
                'message': '商品不存在',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'code': 500,
                'message': f'设置失败: {str(e)}',
                'data': None,
                'timestamp': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)