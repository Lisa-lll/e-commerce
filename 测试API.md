# 测试 API 接口

## 🔍 快速测试后端 API

### 方法 1：使用浏览器

直接在浏览器中访问以下 URL：

1. **商品列表**：
   ```
   http://localhost:8000/api/v1/products/
   ```

2. **商品详情**（替换 {id} 为实际商品ID）：
   ```
   http://localhost:8000/api/v1/products/1/
   ```

3. **分类列表**：
   ```
   http://localhost:8000/api/v1/categories/
   ```

### 方法 2：使用 curl（PowerShell）

```powershell
# 测试商品列表
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/products/" -UseBasicParsing | Select-Object -ExpandProperty Content

# 或者使用 curl（如果已安装）
curl http://localhost:8000/api/v1/products/
```

### 方法 3：使用 Python 脚本

```python
import requests

response = requests.get('http://localhost:8000/api/v1/products/')
print(response.json())
```

## 📋 预期响应格式

### 商品列表响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "results": [
      {
        "id": 1,
        "name": "iPhone 15 Pro Max",
        "subtitle": "苹果最新旗舰手机",
        "price": "8999.00",
        "original_price": "9999.00",
        "stock": 50,
        "sales_count": 0,
        "status": 1,
        "category_id": 2,
        "category_name": "手机",
        "main_image_url": null,
        "created_at": "2026-01-13T10:30:00Z"
      }
    ],
    "count": 12,
    "next": null,
    "previous": null
  },
  "timestamp": null
}
```

## ⚠️ 常见问题

### 问题 1：返回空数组

**可能原因**：
- 商品状态为 0（已下架）
- 查询条件过滤掉了所有商品

**解决方法**：
```python
# 检查商品状态
from products.models import Product
Product.objects.all().values('id', 'name', 'status')
```

### 问题 2：返回 404

**可能原因**：
- URL 路径错误
- 后端服务未启动

**解决方法**：
- 检查后端服务：http://localhost:8000/health
- 检查 URL 路径是否正确

### 问题 3：返回 500 错误

**可能原因**：
- 数据库连接问题
- 序列化器错误

**解决方法**：
- 查看后端日志
- 检查数据库连接

## 🔧 调试步骤

1. **检查后端服务**
   ```bash
   # 访问健康检查
   http://localhost:8000/health
   ```

2. **检查数据库数据**
   ```bash
   python manage.py shell
   from products.models import Product
   Product.objects.count()
   Product.objects.all().values('id', 'name', 'status')
   ```

3. **测试 API 接口**
   ```bash
   # 在浏览器中访问
   http://localhost:8000/api/v1/products/
   ```

4. **检查前端请求**
   - 打开浏览器开发者工具（F12）
   - 查看 Network 标签
   - 检查 API 请求和响应
