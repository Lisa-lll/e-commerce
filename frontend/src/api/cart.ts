import api from './index';
import type { Product } from './products';

export interface CartItem {
  id: number;
  product: Product;
  product_id: number;
  quantity: number;
  created_at: string;
  updated_at: string;
}

// 获取购物车列表（登录用户）
export const getCart = () => {
  return api.get('/cart/');
};

// 添加商品到购物车
export const addToCart = (product_id: number, quantity: number = 1) => {
  return api.post('/cart/add/', {
    product_id,
    quantity,
  });
};

// 更新购物车商品数量
export const updateCartItem = (id: number, quantity: number) => {
  return api.patch(`/cart/${id}/`, { quantity });
};

// 删除购物车商品
export const removeCartItem = (id: number) => {
  return api.delete(`/cart/${id}/`);
};

// 清空购物车
export const clearCart = () => {
  return api.delete('/cart/clear/');
};
