# 知序 Zhixu

> 遣词作序，静揽人间文柔

融合轻文艺内容与英语学习的 Web 应用。每日精选一句/一曲/一文，结合打字练习、默写、错题本，让英语学习成为一种宁静的习惯。

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue 3 + TypeScript + Vite + Tailwind CSS + Pinia |
| 后端 | FastAPI + SQLModel + JWT 认证 |
| 数据库 | SQLite（开发）/ MySQL 8.0（生产） |
| 部署 | Docker Compose + Nginx |

## 快速开始

### Docker 部署（推荐）

```bash
docker compose up -d --build
```

- 前端：http://localhost:1234
- 后端 API 文档：http://localhost:8888/docs
- MySQL：localhost:13306

### 本地开发

**后端**

```bash
cd backend
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

**前端**

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

### 默认账号

| 账号 | 密码 | 角色 |
|------|------|------|
| admin | admin123 | 管理员 |
| demo | demo123 | 普通用户（500 积分，Lv.3） |

## 功能

### 文艺留声 · 每日精选
- **每日一句**：哲理名言卡片，支持收藏、TTS 朗读
- **每日一曲**：音乐推荐卡片，支持收藏
- **每日一文**：文章阅读卡片，支持收藏、弹窗阅读

### 单词簿 · 键盘学习
- **打字练习**：逐字符输入，实时绿/红反馈，强制纠错，自动发音
- **默写模式**：隐藏拼写，根据中文释义自由输入
- **错题本**：自动收集错误单词，按错误次数排序
- **学习看板**：今日/累计统计，积分与等级

### 内置词库

| 词库 | 词条数 |
|------|--------|
| CET-4 大学英语四级 | 4428 |
| CET-6 大学英语六级 | 5523 |

支持通过后台管理批量导入更多词库。

### 用户体系
- 注册/登录（JWT 认证）
- 个人中心（昵称编辑、头像上传）
- 每日签到（日历视图、连续签到奖励）
- 收藏夹（按类型展示收藏内容）

### 排行榜（6 种）
积分总榜 / 月榜 / 周榜 / 今日榜 / 速度之王榜 / 错题攻克榜

### 积分与等级

| 等级 | 积分 | 称号 |
|------|------|------|
| Lv.1 | 0 | 文艺学徒 |
| Lv.2 | 200 | 单词小生 |
| Lv.3 | 500 | 笔墨行者 |
| Lv.4 | 1000 | 浮光阅者 |
| Lv.5 | 2000 | 英文探路者 |
| Lv.6 | 3500 | 星夜记忆者 |
| Lv.7 | 5500 | 轻文艺学士 |
| Lv.8 | 8000 | 键盘诗人 |
| Lv.9 | 12000 | 安宁守护者 |
| Lv.10 | 18000 | 独行大师 |

### 后台管理（管理员）
- 内容管理：筛选、创建、编辑、删除每日内容
- 词库管理：创建词库、批量导入单词、删除词库
- 用户管理：角色切换、重置密码、删除账号

## 项目结构

```
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── requirements.txt
│   ├── data/                  # 种子数据
│   └── app/
│       ├── main.py            # FastAPI 入口
│       ├── models.py          # 数据模型（8 张表）
│       ├── auth.py            # 认证 + 用户资料
│       ├── seed.py            # 种子数据导入
│       ├── routers/           # daily, words, leaderboard, points, admin
│       └── services/          # 积分计算, 排行榜查询
└── frontend/
    ├── Dockerfile
    ├── nginx.conf
    └── src/
        ├── views/             # 16 个页面
        ├── components/        # 8 个组件
        ├── stores/            # Pinia 状态
        ├── api/               # Axios 请求层
        └── router/            # 路由 + 登录守卫
```

## 设计

- **主题色**：暮蓝 `#2C3E50` · 暖米 `#F5F0E6` · 点缀金 `#D4AF37`
- **风格**：极简、留白、温暖，CSS 动画（fadeIn / slideUp / cardAppear）
- **响应式**：桌面端下拉导航，移动端汉堡菜单

## License

MIT
