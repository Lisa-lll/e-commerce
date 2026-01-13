import api from './index';

export interface OrderItem {
  id: number;
  product_id: number;
  product_name: string;
  product_image?: string;
  price: string;
  quantity: number;
  total_amount: string;
}

export interface Order {
  id: number;
  order_no: string;
  user_id?: number;
  status: number;
  status_display: string;
  total_amount: string;
  freight_amount: string;
  pay_amount: string;
  receiver_name: string;
  receiver_phone: string;
  receiver_address: string;
  remark?: string;
  items: OrderItem[];
  created_at: string;
  updated_at: string;
}

// 创建订单（支持未登录用户）
export const createOrder = (data: {
  receiver_name: string;
  receiver_phone: string;
  receiver_address: string;
  remark?: string;
  items: Array<{
    product_id: number;
    quantity: number;
  }>;
}) => {
  return api.post('/orders/', data);
};

// 获取订单列表（登录用户）
export const getOrders = () => {
  return api.get('/orders/');
};

// 获取订单详情
export const getOrderDetail = (id: number) => {
  return api.get(`/orders/${id}/`);
};

// 查询订单（未登录用户通过订单号和手机号）
export const queryOrder = (order_no: string, receiver_phone: string) => {
  return api.post('/orders/query/', {
    order_no,
    receiver_phone,
  });
};
