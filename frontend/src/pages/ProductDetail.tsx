import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Spin, message, Button, InputNumber, Card, Image } from 'antd';
import { ShoppingCartOutlined } from '@ant-design/icons';
import { getProductDetail, type ProductDetail } from '../api/products';
import { addToLocalCart } from '../utils/cart';
import './ProductDetail.css';

const ProductDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [product, setProduct] = useState<ProductDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    if (id) {
      loadProduct();
    }
  }, [id]);

  const loadProduct = async () => {
    try {
      setLoading(true);
      const response = await getProductDetail(Number(id));
      if (response.code === 200) {
        setProduct(response.data);
      }
    } catch (error: any) {
      message.error(error.message || '加载商品详情失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = () => {
    if (!product) return;

    if (quantity > product.stock) {
      message.warning('库存不足');
      return;
    }

    addToLocalCart({
      product_id: product.id,
      product_name: product.name,
      product_image: product.main_image_url,
      price: product.price,
      quantity,
    });

    message.success('已添加到购物车');
  };

  const handleBuyNow = () => {
    if (!product) return;

    if (quantity > product.stock) {
      message.warning('库存不足');
      return;
    }

    // 添加到购物车并跳转到订单页面
    addToLocalCart({
      product_id: product.id,
      product_name: product.name,
      product_image: product.main_image_url,
      price: product.price,
      quantity,
    });

    navigate('/order/create');
  };

  if (loading) {
    return (
      <div className="loading-container">
        <Spin size="large" />
      </div>
    );
  }

  if (!product) {
    return <div>商品不存在</div>;
  }

  return (
    <div className="product-detail">
      <div className="product-detail-content">
        <div className="product-images">
          {product.main_image_url ? (
            <Image src={product.main_image_url} alt={product.name} />
          ) : (
            <div className="no-image">暂无图片</div>
          )}
          {product.images && product.images.length > 0 && (
            <div className="product-images-list">
              {product.images.map((img) => (
                <img key={img.id} src={img.image_url} alt={product.name} />
              ))}
            </div>
          )}
        </div>

        <div className="product-info">
          <h1>{product.name}</h1>
          {product.subtitle && <p className="subtitle">{product.subtitle}</p>}

          <div className="price-section">
            <span className="price">¥{product.price}</span>
            {product.original_price && (
              <span className="original-price">¥{product.original_price}</span>
            )}
          </div>

          <div className="product-meta">
            <div>库存：{product.stock}</div>
            <div>销量：{product.sales_count}</div>
            <div>浏览量：{product.view_count}</div>
          </div>

          <div className="quantity-section">
            <span>数量：</span>
            <InputNumber
              min={1}
              max={product.stock}
              value={quantity}
              onChange={(value) => setQuantity(value || 1)}
            />
          </div>

          <div className="actions">
            <Button
              type="default"
              size="large"
              icon={<ShoppingCartOutlined />}
              onClick={handleAddToCart}
            >
              加入购物车
            </Button>
            <Button type="primary" size="large" onClick={handleBuyNow}>
              立即购买
            </Button>
          </div>

          {product.detail && (
            <Card title="商品详情" style={{ marginTop: 20 }}>
              <div dangerouslySetInnerHTML={{ __html: product.detail }} />
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductDetailPage;
