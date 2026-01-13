# 电商系统管理后台（简化版）

## 技术栈

- React 18
- TypeScript
- Vite
- React Router v6
- Zustand（状态管理）
- Axios
- Ant Design

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

管理后台将运行在 http://localhost:5174

## 项目结构

```
admin/
├── src/
│   ├── api/             # API 接口封装
│   ├── components/      # 通用组件
│   ├── pages/           # 页面组件
│   │   ├── Dashboard/   # 仪表盘
│   │   ├── Products/    # 商品管理
│   │   ├── Orders/      # 订单管理
│   │   ├── Users/       # 用户管理
│   │   └── Categories/  # 分类管理
│   ├── layout/          # 布局组件
│   ├── hooks/           # 自定义 Hooks
│   ├── store/           # 状态管理
│   ├── utils/           # 工具函数
│   ├── types/           # TypeScript 类型
│   └── App.tsx          # 根组件
└── public/              # 静态资源
```

## 功能模块

- 商品管理（上架/下架、编辑、分类管理）
- 订单管理（查询、状态修改）
- 用户管理（查询、状态管理）
- 数据统计（基础统计）

## 开发命令

- `npm run dev` - 启动开发服务器
- `npm run build` - 构建生产版本
- `npm run preview` - 预览生产构建
- `npm run lint` - 代码检查
