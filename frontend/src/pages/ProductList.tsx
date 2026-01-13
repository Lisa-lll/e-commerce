import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Card, Row, Col, Input, Select, Spin, message, Pagination } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import { getProducts, getCategories, type Product, type Category } from '../api/products';
import './ProductList.css';

const { Search } = Input;
const { Option } = Select;

const ProductList = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [categoryId, setCategoryId] = useState<number | undefined>(
    searchParams.get('category_id') ? Number(searchParams.get('category_id')) : undefined
  );
  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [priceOrder, setPriceOrder] = useState<'asc' | 'desc' | undefined>();
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(12);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    loadCategories();
  }, []);

  useEffect(() => {
    setCurrentPage(1); // 筛选条件变化时重置到第一页
    loadProducts();
  }, [categoryId, search, priceOrder]);

  useEffect(() => {
    loadProducts();
  }, [currentPage, pageSize]);

  const loadCategories = async () => {
    try {
      const response = await getCategories();
      if (response.code === 200) {
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
      if (categoryId) params.category_id = categoryId;
      if (search) params.search = search;
      if (priceOrder) params.price_order = priceOrder;

      const response = await getProducts(params);
      if (response && response.code === 200) {
        // 处理分页数据
        if (response.data?.results && Array.isArray(response.data.results)) {
          setProducts(response.data.results);
          setTotal(response.data.count || 0);
        } else if (response.data?.count !== undefined) {
          // DRF 默认分页格式
          setProducts(response.data.results || []);
          setTotal(response.data.count || 0);
        } else if (Array.isArray(response.data)) {
          setProducts(response.data);
          setTotal(response.data.length);
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
      message.error(error.message || '加载商品失败');
      setProducts([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (value: string) => {
    setSearch(value);
    const params = new URLSearchParams();
    if (value) params.set('search', value);
    if (categoryId) params.set('category_id', String(categoryId));
    setSearchParams(params);
  };

  return (
    <div className="product-list">
      <div className="product-list-header">
        <h1>商品列表</h1>
        <div className="filters">
          <Select
            placeholder="选择分类"
            style={{ width: 150, marginRight: 10 }}
            allowClear
            value={categoryId}
            onChange={(value) => {
              setCategoryId(value);
              const params = new URLSearchParams();
              if (value) params.set('category_id', String(value));
              if (search) params.set('search', search);
              setSearchParams(params);
            }}
          >
            <Option value={undefined}>全部分类</Option>
            {categories.map((cat) => (
              <Option key={cat.id} value={cat.id}>
                {cat.name}
              </Option>
            ))}
          </Select>
          <Search
            placeholder="搜索商品"
            allowClear
            enterButton={<SearchOutlined />}
            size="large"
            style={{ width: 300 }}
            onSearch={handleSearch}
            defaultValue={search}
          />
          <Select
            placeholder="价格排序"
            style={{ width: 150, marginLeft: 10 }}
            allowClear
            onChange={(value) => setPriceOrder(value)}
          >
            <Option value="asc">价格从低到高</Option>
            <Option value="desc">价格从高到低</Option>
          </Select>
        </div>
      </div>

      {loading ? (
        <div className="loading-container">
          <Spin size="large" />
        </div>
      ) : (
        <Row gutter={[16, 16]}>
          {products.length === 0 ? (
            <Col span={24}>
              <div style={{ textAlign: 'center', padding: 40 }}>
                暂无商品
              </div>
            </Col>
          ) : (
            products.map((product) => (
              <Col xs={12} sm={8} md={6} key={product.id}>
                <Link to={`/products/${product.id}`}>
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
                          }}
                        >
                          暂无图片
                        </div>
                      )
                    }
                  >
                    <Card.Meta
                      title={product.name}
                      description={
                        <div>
                          <div style={{ color: '#ff4d4f', fontSize: 18, fontWeight: 'bold' }}>
                            ¥{product.price}
                          </div>
                          {product.original_price && (
                            <div style={{ color: '#999', textDecoration: 'line-through', fontSize: 12 }}>
                              ¥{product.original_price}
                            </div>
                          )}
                        </div>
                      }
                    />
                  </Card>
                </Link>
              </Col>
            ))
          )}
        </Row>
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

export default ProductList;
