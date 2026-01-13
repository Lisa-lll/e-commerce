#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建测试商品数据"""

import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Category, Product, ProductImage
from decimal import Decimal

# 商品分类数据
categories_data = [
    {'name': '电子产品', 'parent_id': 0, 'sort_order': 1},
    {'name': '手机', 'parent_id': 0, 'sort_order': 2},
    {'name': '电脑', 'parent_id': 0, 'sort_order': 3},
    {'name': '服装', 'parent_id': 0, 'sort_order': 4},
    {'name': '食品', 'parent_id': 0, 'sort_order': 5},
]

# 商品数据
products_data = [
    {
        'name': 'iPhone 15 Pro Max',
        'subtitle': '苹果最新旗舰手机，A17 Pro芯片，钛金属设计',
        'price': Decimal('8999.00'),
        'original_price': Decimal('9999.00'),
        'stock': 50,
        'category_name': '手机',
        'detail': '<p>iPhone 15 Pro Max 采用钛金属设计，配备A17 Pro芯片，性能强劲。6.7英寸超视网膜XDR显示屏，支持ProMotion自适应刷新率技术。</p>'
    },
    {
        'name': '华为 Mate 60 Pro',
        'subtitle': '华为旗舰手机，麒麟9000S芯片，支持卫星通信',
        'price': Decimal('6999.00'),
        'original_price': Decimal('7999.00'),
        'stock': 30,
        'category_name': '手机',
        'detail': '<p>华为Mate 60 Pro搭载麒麟9000S芯片，支持卫星通信功能。6.82英寸OLED曲面屏，5000mAh大电池，支持66W快充。</p>'
    },
    {
        'name': 'MacBook Pro 14英寸',
        'subtitle': '苹果专业笔记本电脑，M3芯片，14.2英寸Liquid Retina XDR显示屏',
        'price': Decimal('14999.00'),
        'original_price': Decimal('16999.00'),
        'stock': 20,
        'category_name': '电脑',
        'detail': '<p>MacBook Pro 14英寸搭载M3芯片，性能提升显著。14.2英寸Liquid Retina XDR显示屏，支持P3广色域。18小时电池续航。</p>'
    },
    {
        'name': '联想 ThinkPad X1 Carbon',
        'subtitle': '商务笔记本电脑，14英寸2.8K屏幕，Intel i7处理器',
        'price': Decimal('9999.00'),
        'original_price': Decimal('11999.00'),
        'stock': 15,
        'category_name': '电脑',
        'detail': '<p>ThinkPad X1 Carbon采用碳纤维材质，轻薄便携。14英寸2.8K IPS屏幕，Intel i7-1365U处理器，16GB内存，512GB SSD。</p>'
    },
    {
        'name': 'AirPods Pro 2',
        'subtitle': '苹果无线降噪耳机，主动降噪，空间音频',
        'price': Decimal('1899.00'),
        'original_price': Decimal('1999.00'),
        'stock': 100,
        'category_name': '电子产品',
        'detail': '<p>AirPods Pro 2支持主动降噪和自适应通透模式，配备H2芯片，音质更出色。支持空间音频和动态头部追踪。</p>'
    },
    {
        'name': '小米平板6 Pro',
        'subtitle': '11英寸2.8K屏幕，骁龙8+处理器，支持手写笔',
        'price': Decimal('2499.00'),
        'original_price': Decimal('2799.00'),
        'stock': 40,
        'category_name': '电子产品',
        'detail': '<p>小米平板6 Pro配备11英寸2.8K LCD屏幕，搭载骁龙8+处理器，支持120Hz刷新率。8600mAh大电池，支持67W快充。</p>'
    },
    {
        'name': 'Nike Air Max 270',
        'subtitle': '运动休闲鞋，气垫缓震，舒适透气',
        'price': Decimal('899.00'),
        'original_price': Decimal('1099.00'),
        'stock': 80,
        'category_name': '服装',
        'detail': '<p>Nike Air Max 270采用Max Air气垫技术，提供出色的缓震效果。透气网眼鞋面，舒适贴合。适合日常运动和休闲穿着。</p>'
    },
    {
        'name': '优衣库 摇粒绒连帽外套',
        'subtitle': '秋冬保暖外套，摇粒绒材质，多色可选',
        'price': Decimal('199.00'),
        'original_price': Decimal('299.00'),
        'stock': 120,
        'category_name': '服装',
        'detail': '<p>优衣库摇粒绒连帽外套采用100%聚酯纤维材质，柔软舒适，保暖性好。连帽设计，多色可选，适合秋冬季节穿着。</p>'
    },
    {
        'name': '三只松鼠 坚果大礼包',
        'subtitle': '混合坚果礼盒装，8种坚果组合，年货必备',
        'price': Decimal('128.00'),
        'original_price': Decimal('168.00'),
        'stock': 200,
        'category_name': '食品',
        'detail': '<p>三只松鼠坚果大礼包包含8种精选坚果：碧根果、夏威夷果、开心果、腰果、巴旦木、核桃、松子、榛子。礼盒包装，适合送礼。</p>'
    },
    {
        'name': '良品铺子 零食大礼包',
        'subtitle': '休闲零食组合装，20种零食，办公室必备',
        'price': Decimal('88.00'),
        'original_price': Decimal('128.00'),
        'stock': 150,
        'category_name': '食品',
        'detail': '<p>良品铺子零食大礼包包含20种精选零食：肉脯、果干、坚果、饼干、糖果等。独立包装，方便携带，适合办公室和休闲时光。</p>'
    },
    {
        'name': 'iPad Air 5',
        'subtitle': '10.9英寸平板电脑，M1芯片，支持Apple Pencil',
        'price': Decimal('4399.00'),
        'original_price': Decimal('4799.00'),
        'stock': 35,
        'category_name': '电子产品',
        'detail': '<p>iPad Air 5配备10.9英寸Liquid Retina显示屏，搭载M1芯片，性能强劲。支持Apple Pencil和Magic Keyboard。</p>'
    },
    {
        'name': 'Sony WH-1000XM5 降噪耳机',
        'subtitle': '索尼头戴式降噪耳机，30小时续航，Hi-Res音质',
        'price': Decimal('2999.00'),
        'original_price': Decimal('3299.00'),
        'stock': 25,
        'category_name': '电子产品',
        'detail': '<p>Sony WH-1000XM5采用V1降噪处理器，提供业界领先的降噪效果。支持LDAC高解析度音频，30小时电池续航。</p>'
    },
]

def create_categories():
    """创建分类"""
    print('正在创建分类...')
    category_map = {}
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'parent_id': cat_data['parent_id'],
                'sort_order': cat_data['sort_order'],
                'is_show': 1
            }
        )
        category_map[cat_data['name']] = category
        if created:
            print(f'  [创建] {category.name}')
        else:
            print(f'  [已存在] {category.name}')
    
    return category_map

def create_products(category_map):
    """创建商品"""
    print('\n正在创建商品...')
    
    for product_data in products_data:
        category_name = product_data.pop('category_name')
        category = category_map.get(category_name)
        
        if not category:
            print(f'  [跳过] {product_data["name"]} - 分类不存在')
            continue
        
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'category': category,
                'subtitle': product_data.get('subtitle', ''),
                'price': product_data['price'],
                'original_price': product_data.get('original_price'),
                'stock': product_data['stock'],
                'detail': product_data.get('detail', ''),
                'status': 1,
                'sort_order': 0
            }
        )
        
        if created:
            print(f'  [创建] {product.name} - {product.price}元')
        else:
            print(f'  [已存在] {product.name}')

if __name__ == '__main__':
    print('=' * 50)
    print('开始创建测试数据...')
    print('=' * 50)
    
    # 创建分类
    category_map = create_categories()
    
    # 创建商品
    create_products(category_map)
    
    print('\n' + '=' * 50)
    print('测试数据创建完成！')
    print('=' * 50)
    print('\n提示：')
    print('  - 可以通过 Django Admin 查看和管理数据')
    print('  - 访问地址: http://localhost:8000/admin')
    print('  - 前端访问: http://localhost:5173')
