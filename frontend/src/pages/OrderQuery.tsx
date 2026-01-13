import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Card, Form, Input, Button, Descriptions, Tag, message, Spin, Table, List } from 'antd';
import { queryOrder, Order } from '../api/orders';
import './OrderQuery.css';

const OrderQuery = () => {
  const [searchParams] = useSearchParams();
  const [form] = Form.useForm();
  const [order, setOrder] = useState<Order | null>(null);
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const orderNo = searchParams.get('order_no');
    if (orderNo) {
      form.setFieldsValue({ order_no: orderNo });
    }
  }, [searchParams]);

  const handleQuery = async (values: any) => {
    try {
      setLoading(true);
      const orderNo = values.order_no?.trim();
      const phone = values.receiver_phone?.trim();
      
      // 至少填写一个
      if (!orderNo && !phone) {
        message.warning('请至少填写订单号或手机号');
        return;
      }
      
      const response = await queryOrder(orderNo || '', phone || '');
      if (response.code === 200) {
        // 判断返回的是单个订单还是订单列表
        if (Array.isArray(response.data)) {
          setOrders(response.data);
          setOrder(null);
          message.success(`找到 ${response.data.length} 个订单`);
        } else {
          setOrder(response.data);
          setOrders([]);
          message.success('查询成功');
        }
      }
    } catch (error: any) {
      message.error(error.message || '查询失败');
      setOrder(null);
      setOrders([]);
    } finally {
      setLoading(false);
    }
  };

  const getStatusTag = (status: number) => {
    const statusMap: Record<number, { text: string; color: string }> = {
      1: { text: '待付款', color: 'orange' },
      2: { text: '待发货', color: 'blue' },
      3: { text: '待收货', color: 'cyan' },
      4: { text: '已完成', color: 'green' },
      5: { text: '已取消', color: 'red' },
    };
    const statusInfo = statusMap[status] || { text: '未知', color: 'default' };
    return <Tag color={statusInfo.color}>{statusInfo.text}</Tag>;
  };

  return (
    <div className="order-query">
      <h1>订单查询</h1>

      <Card style={{ marginBottom: 20 }}>
        <Form form={form} onFinish={handleQuery} layout="inline">
          <Form.Item
            name="order_no"
            label="订单号"
          >
            <Input placeholder="请输入订单号（可选）" style={{ width: 200 }} />
          </Form.Item>

          <Form.Item
            name="receiver_phone"
            label="手机号"
            rules={[
              { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号' },
            ]}
          >
            <Input placeholder="请输入手机号（可选）" style={{ width: 200 }} />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              查询
            </Button>
          </Form.Item>
        </Form>
        <div style={{ marginTop: 10, color: '#666', fontSize: 12 }}>
          提示：至少填写订单号或手机号其中一个即可查询
        </div>
      </Card>

      {loading ? (
        <div className="loading-container">
          <Spin size="large" />
        </div>
      ) : order ? (
        <Card title="订单详情">
          <Descriptions column={2} bordered>
            <Descriptions.Item label="订单号">{order.order_no}</Descriptions.Item>
            <Descriptions.Item label="订单状态">{getStatusTag(order.status)}</Descriptions.Item>
            <Descriptions.Item label="收货人">{order.receiver_name}</Descriptions.Item>
            <Descriptions.Item label="收货电话">{order.receiver_phone}</Descriptions.Item>
            <Descriptions.Item label="收货地址" span={2}>
              {order.receiver_address}
            </Descriptions.Item>
            <Descriptions.Item label="订单金额">¥{order.total_amount}</Descriptions.Item>
            <Descriptions.Item label="运费">¥{order.freight_amount}</Descriptions.Item>
            <Descriptions.Item label="实付金额">
              <strong style={{ color: '#ff4d4f', fontSize: 18 }}>¥{order.pay_amount}</strong>
            </Descriptions.Item>
            <Descriptions.Item label="创建时间">{order.created_at}</Descriptions.Item>
            {order.remark && (
              <Descriptions.Item label="备注" span={2}>
                {order.remark}
              </Descriptions.Item>
            )}
          </Descriptions>

          <div style={{ marginTop: 20 }}>
            <h3>订单商品</h3>
            <Table
              columns={[
                { title: '商品名称', dataIndex: 'product_name', key: 'product_name' },
                { title: '单价', dataIndex: 'price', key: 'price', render: (p) => `¥${p}` },
                { title: '数量', dataIndex: 'quantity', key: 'quantity' },
                { title: '小计', dataIndex: 'total_amount', key: 'total_amount', render: (t) => `¥${t}` },
              ]}
              dataSource={order.items}
              rowKey="id"
              pagination={false}
            />
          </div>
        </Card>
      ) : orders.length > 0 ? (
        <Card title={`找到 ${orders.length} 个订单`}>
          <div className="orders-list">
            {orders.map((orderItem) => (
              <Card 
                key={orderItem.id || orderItem.order_no} 
                style={{ marginBottom: 16 }} 
                title={`订单号: ${orderItem.order_no}`}
              >
                <Descriptions column={2} size="small" bordered>
                  <Descriptions.Item label="订单状态">{getStatusTag(orderItem.status)}</Descriptions.Item>
                  <Descriptions.Item label="实付金额">
                    <strong style={{ color: '#ff4d4f' }}>¥{orderItem.pay_amount}</strong>
                  </Descriptions.Item>
                  <Descriptions.Item label="收货人">{orderItem.receiver_name}</Descriptions.Item>
                  <Descriptions.Item label="收货电话">{orderItem.receiver_phone}</Descriptions.Item>
                  <Descriptions.Item label="创建时间" span={2}>{orderItem.created_at}</Descriptions.Item>
                </Descriptions>
                <Button 
                  type="primary" 
                  style={{ marginTop: 16 }}
                  onClick={() => {
                    setOrder(orderItem);
                    setOrders([]);
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                  }}
                >
                  查看详情
                </Button>
              </Card>
            ))}
          </div>
        </Card>
      ) : (
        <Card>
          <div style={{ textAlign: 'center', padding: 40, color: '#999' }}>
            请输入订单号或手机号查询订单（至少填写一个）
          </div>
        </Card>
      )}
    </div>
  );
};

export default OrderQuery;
