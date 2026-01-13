# API 使用说明

## 商品创建 API（支持图片上传）

### 创建商品并上传图片

**接口地址：** `POST /api/v1/products/products/`

**请求方法：** POST

**请求类型：** multipart/form-data

**请求参数：**
- `category_id`: 分类ID（必需）
- `name`: 商品名称（必需）
- `subtitle`: 商品副标题（可选）
- `detail`: 商品详情（可选）
- `price`: 商品价格（必需）
- `original_price`: 原价（可选）
- `stock`: 库存（必需）
- `status`: 状态，1-上架，0-下架（默认1）
- `sort_order`: 排序（默认0）
- `main_image`: 主图文件（可选，如果提供会自动设置为商品主图）
- `images[]`: 多张图片文件（可选，可上传多张）

**响应示例：**
```json
{
  "code": 200,
  "message": "商品创建成功",
  "data": {
    "id": 1,
    "name": "商品名称",
    "main_image_url": "/uploads/products/1/20260101120000_0.jpg",
    "images": [
      {
        "id": 1,
        "image_url": "/uploads/products/1/20260101120000_0.jpg",
        "sort_order": 0
      }
    ],
    ...
  },
  "timestamp": null
}
```

**使用示例（curl）：**
```bash
curl -X POST http://localhost:8000/api/v1/products/products/ \
  -F "category_id=1" \
  -F "name=测试商品" \
  -F "price=99.00" \
  -F "stock=100" \
  -F "main_image=@/path/to/main.jpg" \
  -F "images[]=@/path/to/image1.jpg" \
  -F "images[]=@/path/to/image2.jpg"
```

**使用示例（JavaScript/FormData）：**
```javascript
const formData = new FormData();
formData.append('category_id', 1);
formData.append('name', '测试商品');
formData.append('price', '99.00');
formData.append('stock', 100);
formData.append('main_image', fileInput.files[0]); // 主图
formData.append('images[]', fileInput1.files[0]); // 图片1
formData.append('images[]', fileInput2.files[0]); // 图片2

fetch('http://localhost:8000/api/v1/products/products/', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

**注意事项：**
1. 如果上传了 `main_image`，会自动设置为商品主图
2. 如果只上传了 `images[]`，第一张图片会自动设置为主图
3. 图片支持格式：jpg, jpeg, png, gif, webp
4. 单张图片最大5MB
5. 图片会保存在 `uploads/products/{product_id}/` 目录下

---

## 订单状态修改 API

### 修改订单状态

**接口地址：** `PATCH /api/v1/orders/{order_id}/update_status/`

**请求方法：** PATCH 或 PUT

**请求参数：**
```json
{
  "status": 2
}
```

**状态值说明：**
- 1: 待付款
- 2: 待发货
- 3: 待收货
- 4: 已完成
- 5: 已取消

**响应示例：**
```json
{
  "code": 200,
  "message": "订单状态更新成功",
  "data": {
    "id": 1,
    "order_no": "ORD202601011200001234",
    "status": 2,
    "status_display": "待发货",
    ...
  },
  "timestamp": null
}
```

**使用示例（curl）：**
```bash
curl -X PATCH http://localhost:8000/api/v1/orders/1/update_status/ \
  -H "Content-Type: application/json" \
  -d '{"status": 2}'
```

---

## 商品图片上传 API

### 上传商品图片

**接口地址：** `POST /api/v1/products/{product_id}/upload_image/`

**请求方法：** POST

**请求类型：** multipart/form-data

**请求参数：**
- `image`: 图片文件（必需）
  - 支持格式：jpg, jpeg, png, gif, webp
  - 最大大小：5MB
- `sort_order`: 排序顺序（可选，默认为已有图片数量）

**响应示例：**
```json
{
  "code": 200,
  "message": "图片上传成功",
  "data": {
    "id": 1,
    "image_url": "/uploads/products/1/20260101120000.jpg",
    "sort_order": 0,
    "created_at": "2026-01-01T12:00:00Z"
  },
  "timestamp": null
}
```

**使用示例（curl）：**
```bash
curl -X POST http://localhost:8000/api/v1/products/1/upload_image/ \
  -F "image=@/path/to/image.jpg" \
  -F "sort_order=0"
```

### 设置商品主图

**接口地址：** `PATCH /api/v1/products/{product_id}/set_main_image/`

**请求方法：** PATCH 或 PUT

**请求参数：**
```json
{
  "image_id": 1
}
```

**响应示例：**
```json
{
  "code": 200,
  "message": "主图设置成功",
  "data": {
    "id": 1,
    "name": "商品名称",
    "main_image_url": "/uploads/products/1/20260101120000.jpg",
    ...
  },
  "timestamp": null
}
```

**使用示例（curl）：**
```bash
curl -X PATCH http://localhost:8000/api/v1/products/1/set_main_image/ \
  -H "Content-Type: application/json" \
  -d '{"image_id": 1}'
```

---

## 注意事项

1. **文件上传目录：** 图片保存在 `backend/uploads/products/{product_id}/` 目录下
2. **文件访问：** 上传的图片可以通过 `http://localhost:8000/uploads/products/{product_id}/{filename}` 访问
3. **自动设置主图：** 如果商品没有主图，上传的第一张图片会自动设置为商品主图
4. **订单状态：** 只能修改为有效的状态值（1-5）
