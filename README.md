# LinScio 门户系统

> LinScio 产品矩阵统一门户 · FastAPI + Vue 3 + MySQL

## 项目结构

```
linscio-portal/
├── api/                    # FastAPI 后端 (api.linscio.com.cn)
│   ├── app/
│   │   ├── core/           # 配置、数据库、安全
│   │   ├── models/         # SQLAlchemy ORM (14 张表)
│   │   ├── schemas/        # Pydantic 请求/响应模型
│   │   ├── api/v1/         # API 路由
│   │   ├── services/       # 业务逻辑 (邮件/COS/CDN/定时任务)
│   │   ├── middleware/     # 速率限制、CORS
│   │   └── utils/          # 工具函数
│   ├── alembic/            # 数据库迁移
│   └── requirements.txt
├── portal/                 # 授权门户 (portal.linscio.com.cn)
├── admin/                  # 管理后台 (admin.linscio.com.cn)
├── www/                    # 品牌主站 (www.linscio.com.cn)
├── medcomm-site/           # MedComm 产品子站 (medcomm.linscio.com.cn)
└── deploy/                 # 部署配置 (Nginx / Supervisor)
```

## 技术选型

| 层级 | 选型 |
|------|------|
| 后端 | Python · FastAPI + SQLAlchemy + Alembic |
| 数据库 | MySQL 8 |
| 前端 (门户/主站) | Vue 3 + Vite + 自定义组件 |
| 前端 (admin) | Vue 3 + Vite + Element Plus |
| 进程管理 | Supervisor |
| Web 服务 | Nginx + Uvicorn |
| 对象存储 | 腾讯云 COS |
| CDN | 腾讯云 CDN (TypeC 防盗链) |

## 快速开始

### 1. 后端

```bash
cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                  # 默认使用 SQLite 本地开发
PYTHONPATH=. alembic upgrade head     # 创建 14 张表
PYTHONPATH=. python scripts/seed.py   # 写入种子数据 (2 个产品 + 管理员)
PYTHONPATH=. uvicorn app.main:app --reload --port 8000
```

### 2. 前端 (以 portal 为例)

```bash
cd portal
npm install
npm run dev    # http://localhost:5173，自动代理 /api → :8000
```

### 3. 管理后台

```bash
cd admin
npm install
npm run dev    # http://localhost:5174
```

### 种子数据

| 类型 | 值 |
|------|----|
| 管理员邮箱 | admin@linscio.com.cn |
| 管理员密码 | admin123456 |
| 产品 | medcomm, schola |

### API 文档

启动后端后访问 http://localhost:8000/docs (Swagger UI)

## 环境变量

复制 `api/.env.example` 为 `api/.env`。

- **本地开发**：默认配置 `DATABASE_URL=sqlite:///./dev.db`，无需安装 MySQL
- **生产部署**：注释掉 `DATABASE_URL`，配置 `DB_HOST / DB_USER / DB_PASSWORD` 连接 MySQL
