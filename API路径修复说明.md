# API 路径修复说明

## ❌ 问题描述

前端请求 API 时返回 404 错误：
- 请求路径：`http://localhost:8000/api/v1/products/products/?page_size=100`
- 错误：`404 (Not Found)`

## 🔍 问题原因

前端 API 路径配置错误，多了一层路径：
- ❌ 错误：`/api/v1/products/products/`（多了一个 `products`）
- ✅ 正确：`/api/v1/products/`

### 后端路由配置

```
backend/ecommerce/urls.py:
  path('api/v1/', include('products.urls'))
  
backend/products/urls.py:
  router.register(r'products', ProductViewSet)
  
实际路径: /api/v1/products/
```

## ✅ 已修复的 API 路径

### 1. 商品 API (`frontend/src/api/products.ts`)

| 功能 | 修复前 | 修复后 |
|------|--------|--------|
| 商品列表 | `/products/products/` | `/products/` |
| 商品详情 | `/products/products/{id}/` | `/products/{id}/` |
| 商品搜索 | `/products/products/search/` | `/products/search/` |
| 分类列表 | `/products/categories/` | `/categories/` |
| 分类树 | `/products/categories/tree/` | `/categories/tree/` |

### 2. 订单 API (`frontend/src/api/orders.ts`)

| 功能 | 修复前 | 修复后 |
|------|--------|--------|
| 创建订单 | `/orders/orders/` | `/orders/` |
| 订单列表 | `/orders/orders/` | `/orders/` |
| 订单详情 | `/orders/orders/{id}/` | `/orders/{id}/` |
| 订单查询 | `/orders/orders/query/` | `/orders/query/` |

### 3. 购物车 API (`frontend/src/api/cart.ts`)

| 功能 | 修复前 | 修复后 |
|------|--------|--------|
| 购物车列表 | `/orders/cart/` | `/cart/` |
| 添加商品 | `/orders/cart/add/` | `/cart/add/` |
| 更新商品 | `/orders/cart/{id}/` | `/cart/{id}/` |
| 删除商品 | `/orders/cart/{id}/` | `/cart/{id}/` |
| 清空购物车 | `/orders/cart/clear/` | `/cart/clear/` |

### 4. 用户 API (`frontend/src/api/auth.ts`)

| 功能 | 修复前 | 修复后 |
|------|--------|--------|
| 用户注册 | `/users/users/register/` | `/users/register/` |
| 用户登录 | `/users/users/login/` | `/users/login/` |
| 用户信息 | `/users/users/profile/` | `/users/profile/` |

## 📋 正确的 API 路径列表

### 商品相关
- `GET /api/v1/products/` - 商品列表
- `GET /api/v1/products/{id}/` - 商品详情
- `GET /api/v1/products/search/` - 商品搜索
- `GET /api/v1/categories/` - 分类列表
- `GET /api/v1/categories/tree/` - 分类树

### 订单相关
- `POST /api/v1/orders/` - 创建订单
- `GET /api/v1/orders/` - 订单列表（登录用户）
- `GET /api/v1/orders/{id}/` - 订单详情
- `POST /api/v1/orders/query/` - 订单查询（未登录用户）

### 购物车相关
- `GET /api/v1/cart/` - 购物车列表
- `POST /api/v1/cart/add/` - 添加商品
- `PATCH /api/v1/cart/{id}/` - 更新商品
- `DELETE /api/v1/cart/{id}/` - 删除商品
- `DELETE /api/v1/cart/clear/` - 清空购物车

### 用户相关
- `POST /api/v1/users/register/` - 用户注册
- `POST /api/v1/users/login/` - 用户登录
- `GET /api/v1/users/profile/` - 用户信息

## 🚀 验证修复

### 1. 重启前端服务

如果前端服务正在运行，需要重启：

```bash
# 停止服务（Ctrl+C）
# 重新启动
cd frontend
npm run dev
```

### 2. 测试 API

在浏览器中访问：
- 商品列表：http://localhost:8000/api/v1/products/
- 应该返回商品数据，不再是 404

### 3. 检查前端页面

访问：http://localhost:5173
- 应该能正常加载商品列表
- 浏览器控制台不应该有 404 错误

## ✅ 修复完成

所有 API 路径已修复，现在应该可以正常访问了！

如果还有问题，请检查：
1. 后端服务是否正常运行（http://localhost:8000/health）
2. 数据库是否有商品数据
3. 浏览器控制台是否有其他错误
