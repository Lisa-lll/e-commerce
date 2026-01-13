import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button, Card, Table, message, Spin } from 'antd';
import { createOrder } from '../api/orders';
import { getLocalCart, clearLocalCart } from '../utils/cart';
import './OrderCreate.css';

const OrderCreate = () => {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [cart, setCart] = useState(getLocalCart());
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    if (cart.length === 0) {
      message.warning('购物车为空，请先添加商品');
      navigate('/');
      return;
    }
    calculateTotal();
  }, [cart]);

  const calculateTotal = () => {
    const sum = cart.reduce((acc, item) => {
      return acc + parseFloat(item.price) * item.quantity;
    }, 0);
    setTotal(sum);
  };

  const handleSubmit = async (values: any) => {
    try {
      setLoading(true);
      const items = cart.map((item) => ({
        product_id: item.product_id,
        quantity: item.quantity,
      }));

      const response = await createOrder({
        receiver_name: values.receiver_name,
        receiver_phone: values.receiver_phone,
        receiver_address: values.receiver_address,
        remark: values.remark || '',
        items,
      });

      if (response.code === 200) {
        message.success('订单创建成功！');
        clearLocalCart();
        navigate(`/order/query?order_no=${response.data.order_no}`);
      }
    } catch (error: any) {
      message.error(error.message || '订单创建失败');
    } finally {
      setLoading(false);
    }
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
      dataIndex: 'quantity',
      key: 'quantity',
    },
    {
      title: '小计',
      key: 'subtotal',
      render: (record: any) => `¥${(parseFloat(record.price) * record.quantity).toFixed(2)}`,
    },
  ];

  return (
    <div className="order-create">
      <h1>创建订单</h1>

      <div className="order-content">
        <Card title="收货信息" style={{ marginBottom: 20 }}>
          <Form form={form} onFinish={handleSubmit} layout="vertical">
            <Form.Item
              name="receiver_name"
              label="收货人姓名"
              rules={[{ required: true, message: '请输入收货人姓名' }]}
            >
              <Input placeholder="请输入收货人姓名" />
            </Form.Item>

            <Form.Item
              name="receiver_phone"
              label="收货人电话"
              rules={[
                { required: true, message: '请输入收货人电话' },
                { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号' },
              ]}
            >
              <Input placeholder="请输入收货人电话" />
            </Form.Item>

            <Form.Item
              name="receiver_address"
              label="收货地址"
              rules={[{ required: true, message: '请输入收货地址' }]}
            >
              <Input.TextArea rows={3} placeholder="请输入详细收货地址" />
            </Form.Item>

            <Form.Item name="remark" label="备注">
              <Input.TextArea rows={2} placeholder="选填" />
            </Form.Item>

            <Form.Item>
              <Button type="primary" htmlType="submit" size="large" loading={loading} block>
                提交订单
              </Button>
            </Form.Item>
          </Form>
        </Card>

        <Card title="订单商品">
          <Table
            columns={columns}
            dataSource={cart}
            rowKey="product_id"
            pagination={false}
            summary={() => (
              <Table.Summary>
                <Table.Summary.Row>
                  <Table.Summary.Cell index={0} colSpan={3}>
                    <strong>总计</strong>
                  </Table.Summary.Cell>
                  <Table.Summary.Cell index={1}>
                    <strong style={{ color: '#ff4d4f', fontSize: 18 }}>
                      ¥{total.toFixed(2)}
                    </strong>
                  </Table.Summary.Cell>
                </Table.Summary.Row>
              </Table.Summary>
            )}
          />
        </Card>
      </div>
    </div>
  );
};

export default OrderCreate;
