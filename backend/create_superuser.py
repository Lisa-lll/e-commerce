#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建 Django 超级管理员"""

import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth import get_user_model
from admins.models import Admin

User = get_user_model()

# 创建 Django 内置超级用户（用于 Django Admin）
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

# 检查并创建 Django 超级用户
if User.objects.filter(username=username).exists():
    user = User.objects.get(username=username)
    if not user.is_superuser:
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        print('[OK] Django 超级管理员已更新！')
    else:
        print(f'Django 超级用户 {username} 已存在')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print('[OK] Django 超级管理员创建成功！')

print(f'   用户名: {username}')
print(f'   密码: {password}')

# 创建业务管理员（用于业务系统）
if Admin.objects.filter(username=username).exists():
    print(f'业务管理员 {username} 已存在')
else:
    admin = Admin.objects.create(
        username=username,
        name='系统管理员',
        status=1
    )
    admin.set_password(password)
    admin.save()
    print('[OK] 业务管理员创建成功！')
    print(f'   用户名: {username}')
    print(f'   密码: {password}')

print('\n提示：')
print('   - Django Admin 访问地址: http://localhost:8000/admin')
print('   - 建议首次登录后修改密码')
