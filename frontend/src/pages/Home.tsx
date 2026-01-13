import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Card, Row, Col, Spin, message, Empty, Button, Select, Pagination } from 'antd';
import { ShoppingCartOutlined, EyeOutlined } from '@ant-design/icons';
import { getProducts, getCategories, type Product, type Category } from '../api/products';
import { addToLocalCart } from '../utils/cart';
import './Home.css';

const { Option } = Select;

const Home = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [categoryId, setCategoryId] = useState<number | undefined>();
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(12);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    loadCategories();
  }, []);

  useEffect(() => {
    setCurrentPage(1); // 分类变化时重置到第一页
    loadProducts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [categoryId]);

  useEffect(() => {
    loadProducts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentPage, pageSize]);

  const loadCategories = async () => {
    try {
      const response = await getCategories();
      if (response && response.code === 200) {
        const categoryList = response.data?.results || response.data || [];
        setCategories(Array.isArray(categoryList) ? categoryList : []);
      }
    } catch (error: any) {
      console.error('加载分类失败:', error);
    }
  };

  const loadProducts = async () => {
    try {
      setLoading(true);
      const params: any = {
        page: currentPage,
        page_size: pageSize,
      };
      if (categoryId) {
        params.category_id = categoryId;
      }
      const response = await getProducts(params);
      
      // 处理不同的响应格式
      if (response) {
        // 格式1: {code: 200, message: 'success', data: {results: [...], count: ...}}
        if (response.code === 200 && response.data) {
          if (response.data.results && Array.isArray(response.data.results)) {
            setProducts(response.data.results);
            setTotal(response.data.count || 0);
          } else if (Array.isArray(response.data)) {
            setProducts(response.data);
            setTotal(response.data.length);
          } else {
            setProducts([]);
            setTotal(0);
          }
        }
        // 格式2: 直接是分页格式 {count: 12, results: [...]}
        else if (response.results && Array.isArray(response.results)) {
          setProducts(response.results);
          setTotal(response.count || 0);
        }
        // 格式3: 直接是数组
        else if (Array.isArray(response)) {
          setProducts(response);
          setTotal(response.length);
        } else {
          setProducts([]);
          setTotal(0);
        }
      } else {
        setProducts([]);
        setTotal(0);
      }
    } catch (error: any) {
      console.error('加载商品失败:', error);
      message.error(error.message || '加载商品失败，请检查后端服务是否启动');
      setProducts([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  };

  const handleAddToCart = (e: React.MouseEvent, product: Product) => {
    e.preventDefault();
    e.stopPropagation();
    
    addToLocalCart({
      product_id: product.id,
      product_name: product.name,
      product_image: product.main_image_url,
      price: product.price,
      quantity: 1,
    });
    
    message.success('已添加到购物车');
  };

  return (
    <div className="home">
      <div className="home-header">
        <h1>欢迎来到黄石小店</h1>
        <p>无需登录即可浏览商品和下单</p>
        <div style={{ marginTop: '20px', display: 'flex', gap: '10px', justifyContent: 'center', alignItems: 'center' }}>
          <Select
            placeholder="选择分类"
            style={{ width: 200 }}
            allowClear
            value={categoryId}
            onChange={(value) => setCategoryId(value)}
          >
            <Option value={undefined}>全部分类</Option>
            {categories.map((cat) => (
              <Option key={cat.id} value={cat.id}>
                {cat.name}
              </Option>
            ))}
          </Select>
          <Button type="primary" size="large" onClick={loadProducts} loading={loading}>
            刷新商品列表
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="loading-container">
          <Spin size="large" />
          <p style={{ marginTop: '20px' }}>正在加载商品...</p>
        </div>
      ) : products.length === 0 ? (
        <Empty
          description="暂无商品"
          image={Empty.PRESENTED_IMAGE_SIMPLE}
        >
          <Button type="primary" onClick={loadProducts}>
            重新加载
          </Button>
        </Empty>
      ) : (
        <>
          <div style={{ marginBottom: '20px', fontSize: '16px', color: '#666' }}>
            共找到 {products.length} 个商品
          </div>
          <div className="products-container">
            <Row gutter={[16, 16]}>
              {products.map((product) => (
                <Col xs={24} sm={12} md={8} lg={6} key={product.id}>
                  <Card
                    hoverable
                    cover={
                      product.main_image_url ? (
                        <img
                          alt={product.name}
                          src={product.main_image_url}
                          style={{ height: 200, objectFit: 'cover' }}
                        />
                      ) : (
                        <div
                          style={{
                            height: 200,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            background: '#f0f0f0',
                            color: '#999',
                          }}
                        >
                          暂无图片
                        </div>
                      )
                    }
                    actions={[
                      <Link to={`/products/${product.id}`} key="view">
                        <EyeOutlined /> 查看详情
                      </Link>,
                      <a
                        href="#"
                        key="cart"
                        onClick={(e) => handleAddToCart(e, product)}
                      >
                        <ShoppingCartOutlined /> 加入购物车
                      </a>,
                    ]}
                  >
                    <Card.Meta
                      title={
                        <Link to={`/products/${product.id}`} style={{ color: '#333' }}>
                          {product.name}
                        </Link>
                      }
                      description={
                        <div>
                          {product.subtitle && (
                            <div style={{ color: '#666', fontSize: '12px', marginBottom: '8px' }}>
                              {product.subtitle}
                            </div>
                          )}
                          <div style={{ color: '#ff4d4f', fontSize: '20px', fontWeight: 'bold' }}>
                            ¥{product.price}
                          </div>
                          {product.original_price && parseFloat(product.original_price) > parseFloat(product.price) && (
                            <div style={{ color: '#999', textDecoration: 'line-through', fontSize: '14px' }}>
                              原价：¥{product.original_price}
                            </div>
                          )}
                          <div style={{ marginTop: '8px', fontSize: '12px', color: '#999' }}>
                            库存：{product.stock} | 销量：{product.sales_count}
                          </div>
                        </div>
                      }
                    />
                  </Card>
                </Col>
              ))}
            </Row>
          </div>
        </>
      )}

      {!loading && products.length > 0 && (
        <div style={{ marginTop: 24, textAlign: 'center' }}>
          <Pagination
            current={currentPage}
            pageSize={pageSize}
            total={total}
            showSizeChanger
            showQuickJumper
            showTotal={(total) => `共 ${total} 个商品`}
            onChange={(page, size) => {
              setCurrentPage(page);
              setPageSize(size);
            }}
            onShowSizeChange={(current, size) => {
              setCurrentPage(1);
              setPageSize(size);
            }}
            pageSizeOptions={['12', '24', '48', '96']}
          />
        </div>
      )}
    </div>
  );
};

export default Home;
