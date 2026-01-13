import { Link, useLocation } from 'react-router-dom';
import { Layout as AntLayout, Menu } from 'antd';
import { HomeOutlined, ShoppingOutlined, ShoppingCartOutlined, FileSearchOutlined } from '@ant-design/icons';
import { getLocalCartCount } from '../utils/cart';
import { useState, useEffect } from 'react';
import './Layout.css';

const { Header, Content, Footer } = AntLayout;

interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const location = useLocation();
  const [cartCount, setCartCount] = useState(0);

  useEffect(() => {
    // 更新购物车数量
    const updateCartCount = () => {
      setCartCount(getLocalCartCount());
    };
    updateCartCount();
    
    // 监听 localStorage 变化
    const interval = setInterval(updateCartCount, 1000);
    return () => clearInterval(interval);
  }, [location]);

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: <Link to="/">首页</Link>,
    },
    {
      key: '/products',
      icon: <ShoppingOutlined />,
      label: <Link to="/products">商品列表</Link>,
    },
    {
      key: '/cart',
      icon: <ShoppingCartOutlined />,
      label: (
        <Link to="/cart">
          购物车 {cartCount > 0 && <span style={{ color: '#ff4d4f' }}>({cartCount})</span>}
        </Link>
      ),
    },
    {
      key: '/order/query',
      icon: <FileSearchOutlined />,
      label: <Link to="/order/query">订单查询</Link>,
    },
  ];

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Header style={{ 
        background: '#fff', 
        padding: '0 50px', 
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        position: 'sticky',
        top: 0,
        zIndex: 100
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap' }}>
          <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#1890ff' }}>
            <Link to="/" style={{ color: '#1890ff', textDecoration: 'none' }}>
              黄石小店
            </Link>
          </div>
          <Menu
            mode="horizontal"
            selectedKeys={[location.pathname]}
            items={menuItems}
            style={{ flex: 1, justifyContent: 'flex-end', border: 'none', minWidth: 0 }}
          />
        </div>
      </Header>
      <Content style={{ padding: '24px 50px', background: '#f0f2f5' }}>
        <div style={{ background: '#fff', padding: '24px', minHeight: 'calc(100vh - 200px)', borderRadius: '8px' }}>
          {children}
        </div>
      </Content>
      <Footer style={{ textAlign: 'center', background: '#fff' }}>
        黄石小店 ©2026 - 无需登录即可下单
      </Footer>
    </AntLayout>
  );
};

export default Layout;
