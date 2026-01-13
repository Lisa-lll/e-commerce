/**
 * 购物车工具函数（localStorage，用于未登录用户）
 */

export interface CartItem {
  product_id: number;
  product_name: string;
  product_image?: string;
  price: string;
  quantity: number;
}

const CART_KEY = 'ecommerce_cart';

// 获取购物车
export const getLocalCart = (): CartItem[] => {
  const cartStr = localStorage.getItem(CART_KEY);
  if (!cartStr) return [];
  try {
    return JSON.parse(cartStr);
  } catch {
    return [];
  }
};

// 保存购物车
export const saveLocalCart = (cart: CartItem[]) => {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
};

// 添加商品到购物车
export const addToLocalCart = (item: CartItem) => {
  const cart = getLocalCart();
  const existingIndex = cart.findIndex((i) => i.product_id === item.product_id);
  
  if (existingIndex >= 0) {
    cart[existingIndex].quantity += item.quantity;
  } else {
    cart.push(item);
  }
  
  saveLocalCart(cart);
  return cart;
};

// 更新购物车商品数量
export const updateLocalCartItem = (product_id: number, quantity: number) => {
  const cart = getLocalCart();
  const index = cart.findIndex((i) => i.product_id === product_id);
  
  if (index >= 0) {
    if (quantity <= 0) {
      cart.splice(index, 1);
    } else {
      cart[index].quantity = quantity;
    }
    saveLocalCart(cart);
  }
  
  return cart;
};

// 删除购物车商品
export const removeLocalCartItem = (product_id: number) => {
  const cart = getLocalCart();
  const newCart = cart.filter((i) => i.product_id !== product_id);
  saveLocalCart(newCart);
  return newCart;
};

// 清空购物车
export const clearLocalCart = () => {
  localStorage.removeItem(CART_KEY);
  return [];
};

// 获取购物车商品总数
export const getLocalCartCount = (): number => {
  const cart = getLocalCart();
  return cart.reduce((sum, item) => sum + item.quantity, 0);
};

// 获取购物车总金额
export const getLocalCartTotal = (): number => {
  const cart = getLocalCart();
  return cart.reduce((sum, item) => {
    return sum + parseFloat(item.price) * item.quantity;
  }, 0);
};
