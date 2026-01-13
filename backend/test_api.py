#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试 API 接口"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.test import Client
import json

client = Client()

# 测试商品列表 API
print("=" * 50)
print("测试商品列表 API")
print("=" * 50)

response = client.get('/api/v1/products/')
print(f"状态码: {response.status_code}")
print(f"响应内容:")
try:
    data = json.loads(response.content)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    if data.get('code') == 200:
        products = data.get('data', {})
        if isinstance(products, dict) and 'results' in products:
            print(f"\n商品数量: {len(products['results'])}")
        elif isinstance(products, list):
            print(f"\n商品数量: {len(products)}")
except Exception as e:
    print(f"解析响应失败: {e}")
    print(f"原始响应: {response.content.decode('utf-8')}")
