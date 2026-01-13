# 电商系统前端（简化版）

## 技术栈

- React 18
- TypeScript
- Vite
- React Router v6
- Zustand（状态管理）
- Axios
- Ant Design（可选）

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

### 3. 启动开发服务器

```bash
npm run dev
```

前端将运行在 http://localhost:5173

## 项目结构

```
frontend/
├── src/
│   ├── api/             # API 接口封装
│   ├── assets/          # 静态资源
│   ├── components/      # 通用组件
│   ├── pages/           # 页面组件
│   │   ├── Home/        # 首页
│   │   ├── Products/    # 商品列表/详情
│   │   ├── Cart/        # 购物车
│   │   ├── Order/       # 订单
│   │   └── User/        # 用户中心（可选）
│   ├── hooks/           # 自定义 Hooks
│   ├── store/           # 状态管理（Zustand）
│   ├── utils/           # 工具函数
│   ├── types/           # TypeScript 类型
│   └── App.tsx          # 根组件
└── public/              # 静态资源
```

## 功能特性

- ✅ 无需登录即可浏览商品和下单
- ✅ 未登录用户购物车使用 localStorage
- ✅ 登录用户购物车使用数据库（多设备同步）
- ✅ 订单查询：未登录用户通过订单号+手机号查询

## 开发命令

- `npm run dev` - 启动开发服务器
- `npm run build` - 构建生产版本
- `npm run preview` - 预览生产构建
- `npm run lint` - 代码检查
