# war3-tournament-hub

Warcraft III / Frozen Throne 中文赛事资讯网站（第一版，Mock 数据）。

## 技术栈

- Next.js (App Router)
- TypeScript
- Tailwind CSS
- Prisma ORM
- PostgreSQL / Supabase（预留）
- Vercel（可直接部署）

## 已实现页面

- `/` 首页：今日赛事、即将开赛、正在直播、最新录像、最新视频
- `/matches` 赛事列表 + 状态筛选
- `/matches/[id]` 比赛详情
- `/replays` 录像列表
- `/videos` 视频列表
- `/players` 选手页
- `/admin` 后台管理（Mock 表单）

## 本地运行

```bash
npm install
npm run dev
```

打开 http://localhost:3000

## 构建

```bash
npm run build
```

## Prisma

1. 复制环境变量
```bash
cp .env.example .env
```
2. 生成客户端
```bash
npm run prisma:generate
```
3. 开发迁移（接入数据库后）
```bash
npm run prisma:migrate
```

## 说明

- 第一版使用 `data/mock.ts`，不依赖外部 API。
- 设计风格为暗色电竞黑金风，移动端适配，卡片式布局。
- 未使用暴雪官方 Logo 或未授权素材。
