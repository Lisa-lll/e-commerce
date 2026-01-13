import api from './index';

export interface User {
  id: number;
  username: string;
  nickname?: string;
  avatar_url?: string;
  status: number;
}

// 用户注册
export const register = (data: {
  username: string;
  password: string;
  nickname?: string;
}) => {
  return api.post('/users/register/', data);
};

// 用户登录
export const login = (username: string, password: string) => {
  return api.post('/users/login/', {
    username,
    password,
  });
};

// 获取当前用户信息
export const getProfile = () => {
  return api.get('/users/profile/');
};

// 退出登录
export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  window.location.href = '/';
};
