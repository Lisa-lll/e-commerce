#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建 .env 文件"""

env_content = """# Django 配置
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 数据库配置
DB_NAME=ecommerce_simple
DB_USER=root
DB_PASSWORD=nihao123
DB_HOST=localhost
DB_PORT=3306

# JWT 配置
JWT_SECRET=your_jwt_secret_key_here_change_in_production
JWT_EXPIRE_DAYS=7

# 文件上传配置
MAX_FILE_SIZE=5242880

# 应用配置
FRONTEND_URL=http://localhost:5173
ADMIN_URL=http://localhost:5174
"""

with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print('.env 文件已创建')
