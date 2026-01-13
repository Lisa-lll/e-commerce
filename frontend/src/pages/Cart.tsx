import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button, InputNumber, Table, message, Empty } from 'antd';
import { DeleteOutlined, ShoppingOutlined } from '@ant-design/icons';
import {
  getLocalCart,
  updateLocalCartItem,
  removeLocalCartItem,
  clearLocalCart,
  getLocalCartTotal,
} from '../utils/cart';
import './Cart.css';

const Cart = () => {
  const navigate = useNavigate();
  const [cart, setCart] = useState(getLocalCart());
  const [total, setTotal] = useState(0);

  useEffect(() => {
    updateTotal();
  }, [cart]);

  const updateTotal = () => {
    setTotal(getLocalCartTotal());
  };

  const handleQuantityChange = (product_id: number, quantity: number) => {
    const newCart = updateLocalCartItem(product_id, quantity);
    setCart(newCart);
  };

  const handleRemove = (product_id: number) => {
    const newCart = removeLocalCartItem(product_id);
    setCart(newCart);
    message.success('已移除');
  };

  const handleClear = () => {
    clearLocalCart();
    setCart([]);
    message.success('购物车已清空');
  };

  const handleCheckout = () => {
    if (cart.length === 0) {
      message.warning('购物车为空');
      return;
    }
    navigate('/order/create');
  };

  const columns = [
    {
      title: '商品',
      key: 'product',
      render: (record: any) => (
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          {record.product_image && (
            <img
              src={record.product_image}
              alt={record.product_name}
              style={{ width: 60, height: 60, objectFit: 'cover' }}
            />
          )}
          <span>{record.product_name}</span>
        </div>
      ),
    },
    {
      title: '单价',
      dataIndex: 'price',
      key: 'price',
      render: (price: string) => `¥${price}`,
    },
    {
      title: '数量',
      key: 'quantity',
      render: (record: any) => (
        <InputNumber
          min={1}
          value={record.quantity}
          onChange={(value) => handleQuantityChange(record.product_id, value || 1)}
        />
      ),
    },
    {
      title: '小计',
      key: 'subtotal',
      render: (record: any) => `¥${(parseFloat(record.price) * record.quantity).toFixed(2)}`,
    },
    {
      title: '操作',
      key: 'action',
      render: (record: any) => (
        <Button
          type="link"
          danger
          icon={<DeleteOutlined />}
          onClick={() => handleRemove(record.product_id)}
        >
          删除
        </Button>
      ),
    },
  ];

  return (
    <div className="cart">
      <h1>购物车</h1>

      {cart.length === 0 ? (
        <Empty description="购物车为空" />
      ) : (
        <>
          <Card>
            <Table
              columns={columns}
              dataSource={cart}
              rowKey="product_id"
              pagination={false}
            />
          </Card>

          <Card className="cart-summary">
            <div className="summary-row">
              <span>总计：</span>
              <span className="total-price">¥{total.toFixed(2)}</span>
            </div>
            <div className="cart-actions">
              <Button onClick={handleClear}>清空购物车</Button>
              <Button type="primary" size="large" icon={<ShoppingOutlined />} onClick={handleCheckout}>
                去结算
              </Button>
            </div>
          </Card>
        </>
      )}
    </div>
  );
};

export default Cart;
