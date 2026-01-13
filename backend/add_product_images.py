#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""为商品添加随机图片URL"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Product

# 使用占位图片服务（Picsum Photos）
# 也可以使用其他图片服务，如：https://via.placeholder.com, https://picsum.photos
IMAGE_BASE_URL = "https://picsum.photos/400/400?random="

products = Product.objects.all()

print(f"开始为 {products.count()} 个商品添加图片...")

for product in products:
    # 为每个商品生成一个随机图片URL（基于商品ID）
    image_url = f"{IMAGE_BASE_URL}{product.id}"
    product.main_image_url = image_url
    product.save(update_fields=['main_image_url'])
    print(f"  [完成] {product.name} - {image_url}")

print("\n所有商品图片已添加完成！")
print("\n提示：")
print("  - 图片使用 Picsum Photos 占位图服务")
print("  - 如需使用真实图片，可以在 Django Admin 中手动上传")
print("  - 或使用其他图片服务替换 IMAGE_BASE_URL")
