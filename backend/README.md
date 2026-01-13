# 电商系统后端（简化版）- Django

## 技术栈

- Python 3.8+
- Django 6.0
- Django REST Framework
- MySQL 8.0
- Django CORS Headers

## 快速开始

### 1. 创建虚拟环境（如果还没有）

```bash
python -m venv venv
```

### 2. 激活虚拟环境

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置数据库连接信息。

### 5. 初始化数据库

```bash
# 创建数据库迁移文件
python manage.py makemigrations

# 执行数据库迁移
python manage.py migrate

# 可选：创建超级管理员（Django admin）
python manage.py createsuperuser
```

### 6. 启动开发服务器

```bash
python manage.py runserver
```

服务器将运行在 http://localhost:8000

## 项目结构

```
backend/
├── ecommerce/           # Django 项目配置
│   ├── settings.py      # 项目设置
│   ├── urls.py         # URL 路由
│   └── utils.py        # 工具函数
├── users/              # 用户应用
│   ├── models.py       # 用户模型
│   ├── views.py        # 视图
│   ├── serializers.py  # 序列化器
│   └── urls.py         # URL 路由
├── products/           # 商品应用
├── orders/             # 订单应用
├── admins/             # 管理员应用
├── manage.py           # Django 管理脚本
├── requirements.txt    # Python 依赖
└── uploads/           # 文件上传目录
```

## 开发命令

- `python manage.py runserver` - 启动开发服务器
- `python manage.py makemigrations` - 创建数据库迁移
- `python manage.py migrate` - 执行数据库迁移
- `python manage.py createsuperuser` - 创建超级管理员
- `python manage.py shell` - Django shell
- `python manage.py collectstatic` - 收集静态文件（生产环境）

## API 文档

API 基础路径：`/api/v1`

### 健康检查

- `GET /health` - 服务健康检查
- `GET /api/v1` - API 版本信息

## 注意事项

- 支持未登录用户下单（Order.user 可为空）
- 购物车：登录用户使用数据库，未登录用户使用 localStorage
- 订单查询：未登录用户通过订单号和手机号查询
- 使用 Django ORM 替代 Prisma
- 文件上传存储在 `uploads/` 目录

## 数据库模型

- `User` - 用户表（可选）
- `UserAddress` - 用户地址表
- `Category` - 商品分类表
- `Product` - 商品表
- `ProductImage` - 商品图片表
- `Order` - 订单表（user 可为空）
- `OrderItem` - 订单商品明细表
- `CartItem` - 购物车表（仅登录用户）
- `Admin` - 管理员表