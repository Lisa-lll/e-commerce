import api from './index';

// 导出类型定义
export type Product = {
  id: number;
  name: string;
  subtitle?: string;
  main_image_url?: string;
  price: string;
  original_price?: string;
  stock: number;
  sales_count: number;
  status: number;
  category_id: number;
  category_name?: string;
  created_at: string;
};

export type ProductDetail = Product & {
  detail?: string;
  view_count: number;
  images?: Array<{
    id: number;
    image_url: string;
    sort_order: number;
  }>;
  category: {
    id: number;
    name: string;
  };
};

export type Category = {
  id: number;
  parent_id: number;
  name: string;
  image_url?: string;
  sort_order: number;
  is_show: number;
};

// 获取商品列表
export const getProducts = (params?: {
  category_id?: number;
  search?: string;
  price_order?: 'asc' | 'desc';
  page?: number;
  page_size?: number;
}) => {
  return api.get('/products/', { params });
};

// 获取商品详情
export const getProductDetail = (id: number) => {
  return api.get(`/products/${id}/`);
};

// 搜索商品
export const searchProducts = (keyword: string) => {
  return api.get('/products/search/', { params: { keyword } });
};

// 获取分类列表
export const getCategories = () => {
  return api.get('/categories/');
};

// 获取分类树
export const getCategoryTree = () => {
  return api.get('/categories/tree/');
};
