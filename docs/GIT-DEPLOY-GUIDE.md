# LinScio Portal — Git 推送 / 拉取 / 云服务器更新 完整指南

> 适用于 linscio-portal 项目。含本机 Git 操作、腾讯云宝塔服务器更新、部署全流程指令。

---

## 目录

1. [GitHub 推送（本机 → GitHub）](#一github-推送本机--github)
2. [GitHub 拉取（本机 ← GitHub）](#二github-拉取本机--github)
3. [腾讯云服务器更新（GitHub → 服务器 → 部署上线）](#三腾讯云服务器更新github--服务器--部署上线)
4. [快速参考命令集](#四快速参考命令集)
5. [Manifest / COS 更新](#五manifest--cos-更新)
6. [常见问题](#六常见问题)

---

## 一、GitHub 推送（本机 → GitHub）

### 1.1 首次推送前准备

```bash
# ── 进入项目目录 ──
cd /Users/xiaoshiqi/linscio/linscio-portal

# ── 初始化 Git（如果还未初始化） ──
git init
git branch -M main

# ── 配置远程仓库（使用 Personal Access Token） ──
# ⚠️ 将 <YOUR_TOKEN> 替换为你的 GitHub PAT
git remote add origin https://<YOUR_TOKEN>@github.com/xiaoshiqi0918/linscio-portal.git

# ── 如果已有 remote，更新 URL ──
git remote set-url origin https://<YOUR_TOKEN>@github.com/xiaoshiqi0918/linscio-portal.git

# ── 验证远程配置 ──
git remote -v
```

### 1.2 每次推送前检查

```bash
cd /Users/xiaoshiqi/linscio/linscio-portal

# ── 查看当前状态：哪些文件改了、哪些未跟踪 ──
git status

# ── 查看具体改了什么（已跟踪文件的差异） ──
git diff

# ── 查看未跟踪的文件 ──
git status --porcelain
```

### 1.3 添加、提交、推送（三步走）

```bash
cd /Users/xiaoshiqi/linscio/linscio-portal

# ── 第一步：添加所有改动到暂存区 ──
git add -A

# ── 第二步：提交（commit message 找我帮你写） ──
git commit -m "你的提交信息"

# ── 第三步：推送到 GitHub ──
git push -u origin main
```

### 1.4 一键推送（确认无误后可用）

```bash
cd /Users/xiaoshiqi/linscio/linscio-portal
git add -A && git commit -m "你的提交信息" && git push -u origin main
```

### 1.5 完整推送示例（含 Token）

```bash
cd /Users/xiaoshiqi/linscio/linscio-portal
git remote set-url origin https://<YOUR_TOKEN>@github.com/xiaoshiqi0918/linscio-portal.git
git add -A
git commit -m "feat: manifest v2.0 + bundle API + MedPic 功能介绍"
git push -u origin main
```

> **安全提醒**：
> - Token 只需在 remote URL 中配置一次，后续 push/pull 自动使用
> - 不要在 commit message 或代码中包含 Token
> - `.env` 文件已在 `.gitignore` 中排除，不会被推送

---

## 二、GitHub 拉取（本机 ← GitHub）

### 2.1 常规拉取

```bash
cd /Users/xiaoshiqi/linscio/linscio-portal

# ── 拉取并合并 ──
git pull origin main
```

### 2.2 有本地改动时拉取

```bash
cd /Users/xiaoshiqi/linscio/linscio-portal

# ── 暂存本地改动 ──
git stash

# ── 拉取最新代码 ──
git pull origin main

# ── 恢复本地改动 ──
git stash pop
```

### 2.3 拉取后重新安装依赖

```bash
cd /Users/xiaoshiqi/linscio/linscio-portal

# ── 后端依赖（如 requirements.txt 有变动） ──
cd api
source venv/bin/activate   # 如果有虚拟环境
pip install -r requirements.txt
cd ..

# ── 前端依赖（如 package.json 有变动） ──
cd portal && npm install && cd ..
cd medcomm-site && npm install && cd ..
cd admin && npm install && cd ..
cd www && npm install && cd ..
```

---

## 三、腾讯云服务器更新（GitHub → 服务器 → 部署上线）

> 服务器环境：
> - 源码位置：`/www/wwwroot/linscio-portal`
> - 静态发布：`/www/wwwroot/linscio-release`
> - API 进程：Supervisor → linscio-api（Uvicorn :8000）
> - 面板：宝塔

### 3.1 首次克隆（全新服务器）

```bash
# ── SSH 登录服务器 ──
ssh root@你的服务器IP

# ── 克隆项目 ──
cd /www/wwwroot
git clone https://<YOUR_TOKEN>@github.com/xiaoshiqi0918/linscio-portal.git
cd linscio-portal

# ── 首次全量部署（含前端构建 + 后端 + 数据库迁移 + Nginx） ──
sudo bash deploy/baota-deploy.sh --seed
```

### 3.2 日常更新（最常用）

每次在本机推送代码到 GitHub 后，在服务器上执行：

```bash
# ── SSH 登录服务器 ──
ssh root@你的服务器IP

# ── 进入项目目录 ──
cd /www/wwwroot/linscio-portal

# ── 拉取最新代码 ──
git pull origin main
```

然后根据改动范围选择部署方式：

#### 方式 A：一键全量部署（推荐，最安全）

```bash
sudo bash deploy/deploy.sh all
```

> 等价于：构建全部前端 → 数据库迁移 → 重启后端 → 重载 Nginx

#### 方式 B：只改了前端

```bash
sudo bash deploy/deploy.sh frontend
```

#### 方式 C：只改了后端 API

```bash
# ── 安装新依赖（如果 requirements.txt 有变动） ──
cd /www/wwwroot/linscio-portal/api
source venv/bin/activate
pip install -r requirements.txt

# ── 数据库迁移（如果有新迁移文件） ──
PYTHONPATH=. alembic upgrade head

# ── 重启 API 服务 ──
supervisorctl restart linscio-api
```

或用 deploy 脚本：

```bash
sudo bash deploy/deploy.sh migrate
sudo bash deploy/deploy.sh backend
```

#### 方式 D：只改了 Nginx 配置

```bash
sudo bash deploy/deploy.sh nginx
```

### 3.3 服务器上有本地改动时更新

```bash
cd /www/wwwroot/linscio-portal

# ── 暂存本地改动 ──
git stash

# ── 拉取最新代码 ──
git pull origin main

# ── 恢复本地改动（如有冲突需手动解决） ──
git stash pop

# ── 部署 ──
sudo bash deploy/deploy.sh all
```

### 3.4 数据安全说明

| 数据类型 | 存储位置 | git pull 是否影响 |
|---------|---------|-----------------|
| 用户数据 / 授权信息 | MySQL 数据库 | ❌ 完全不影响 |
| `.env` 配置文件 | `api/.env` | ❌ 在 .gitignore 中 |
| SQLite 开发数据库 | `*.db` / `*.sqlite` | ❌ 在 .gitignore 中 |
| 上传文件 | COS 云存储 | ❌ 不在仓库中 |
| 日志 | `/www/wwwroot/linscio-release/logs/` | ❌ 在 .gitignore 中 |
| 源代码 | `/www/wwwroot/linscio-portal/` | ✅ 会更新（这就是目的） |
| 构建产物 | `*/dist/` | ❌ 在 .gitignore 中，需重新构建 |

---

## 四、快速参考命令集

### 本机 → GitHub 推送

```bash
# 完整命令集（复制粘贴即用，修改 commit message）
cd /Users/xiaoshiqi/linscio/linscio-portal
git remote set-url origin https://<YOUR_TOKEN>@github.com/xiaoshiqi0918/linscio-portal.git
git add -A
git commit -m "你的提交信息"
git push -u origin main
```

### GitHub → 本机 拉取

```bash
cd /Users/xiaoshiqi/linscio/linscio-portal
git pull origin main
```

### GitHub → 服务器 → 上线（完整流程）

```bash
# 在服务器上执行
ssh root@你的服务器IP
cd /www/wwwroot/linscio-portal
git pull origin main
sudo bash deploy/deploy.sh all
```

### 服务器只更新后端

```bash
ssh root@你的服务器IP
cd /www/wwwroot/linscio-portal
git pull origin main
sudo bash deploy/deploy.sh backend
```

### 服务器只更新前端

```bash
ssh root@你的服务器IP
cd /www/wwwroot/linscio-portal
git pull origin main
sudo bash deploy/deploy.sh frontend
```

### 查看服务状态

```bash
# API 状态
supervisorctl status linscio-api

# API 日志
tail -50 /www/wwwroot/linscio-release/logs/api.log
tail -50 /www/wwwroot/linscio-release/logs/api_error.log

# API 健康检查
curl -s http://127.0.0.1:8000/health

# Nginx 状态
nginx -t
systemctl status nginx
```

### 服务器紧急重启

```bash
# 重启 API
supervisorctl restart linscio-api

# 重启 Nginx
systemctl reload nginx
```

---

## 五、Manifest / COS 更新

当更新 `manifest.json`（新版本、新组件包等）后：

### 5.1 更新本地 manifest.json

编辑 `/Users/xiaoshiqi/linscio/linscio-portal/manifest.json`

### 5.2 上传到 COS

```bash
# ── 安装 coscli（首次） ──
# macOS (Apple Silicon)
curl -sSL https://github.com/tencentyun/coscli/releases/download/v1.0.8/coscli-v1.0.8-darwin-arm64 -o /usr/local/bin/coscli
chmod +x /usr/local/bin/coscli

# ── 配置（首次） ──
coscli config set \
  --secret-id "你的SecretId" \
  --secret-key "你的SecretKey"

# ── 上传 manifest.json 到学科包桶 ──
coscli cp manifest.json "cos://linscio-specialties-1363203425/manifest.json"

# ── 验证上传 ──
coscli ls "cos://linscio-specialties-1363203425/manifest.json"
```

### 5.3 同步推送到 GitHub

```bash
cd /Users/xiaoshiqi/linscio/linscio-portal
git add manifest.json
git commit -m "chore: 更新 manifest.json - 版本号/组件包信息"
git push origin main
```

### 5.4 更新服务器（API 读的是 COS 上的 manifest.json，但代码中也有一份作为备份）

```bash
ssh root@你的服务器IP
cd /www/wwwroot/linscio-portal
git pull origin main
# API 不需要重启（read_manifest() 每次从 COS 实时读取）
```

---

## 六、常见问题

### Q: git push 被拒绝 (rejected)

```bash
# 先拉取合并再推送
git pull origin main --rebase
git push origin main
```

### Q: 服务器 git pull 时提示文件冲突

```bash
cd /www/wwwroot/linscio-portal

# 方式一：暂存再恢复
git stash
git pull origin main
git stash pop

# 方式二：丢弃本地改动（⚠️ 会丢失服务器上的手动改动）
git checkout .
git pull origin main
```

### Q: npm ci 报错 lockfile 不匹配

```bash
# 删除 node_modules 后重新安装
rm -rf node_modules
npm install
```

### Q: API 启动失败

```bash
# 查看详细错误
supervisorctl status linscio-api
tail -100 /www/wwwroot/linscio-release/logs/api_error.log

# 手动测试启动
cd /www/wwwroot/linscio-portal/api
source venv/bin/activate
PYTHONPATH=. uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Q: 数据库迁移失败

```bash
cd /www/wwwroot/linscio-portal/api
source venv/bin/activate

# 查看当前迁移状态
PYTHONPATH=. alembic current

# 查看待执行迁移
PYTHONPATH=. alembic history

# 执行迁移
PYTHONPATH=. alembic upgrade head
```

### Q: 前端构建后页面白屏

```bash
# 确认静态文件是否正确发布
ls -la /www/wwwroot/linscio-release/portal/
ls -la /www/wwwroot/linscio-release/medcomm/

# 确认 Nginx 配置中 root 指向正确
nginx -t
cat /etc/nginx/conf.d/portal.linscio.com.cn.conf | grep root

# 重载 Nginx
systemctl reload nginx
```

### Q: Token 过期或无权限

```bash
# 在 GitHub → Settings → Developer Settings → Personal Access Tokens 重新生成
# 然后更新 remote URL
cd /Users/xiaoshiqi/linscio/linscio-portal
git remote set-url origin https://<NEW_TOKEN>@github.com/xiaoshiqi0918/linscio-portal.git

# 服务器上也需要更新
ssh root@你的服务器IP
cd /www/wwwroot/linscio-portal
git remote set-url origin https://<NEW_TOKEN>@github.com/xiaoshiqi0918/linscio-portal.git
```

---

## 附录：deploy.sh 命令速查

| 命令 | 作用 |
|------|------|
| `sudo bash deploy/deploy.sh all` | 全量部署（前端+迁移+后端+Nginx） |
| `sudo bash deploy/deploy.sh frontend` | 仅构建并部署前端 |
| `sudo bash deploy/deploy.sh backend` | 仅安装依赖+重启 API |
| `sudo bash deploy/deploy.sh migrate` | 仅执行数据库迁移 |
| `sudo bash deploy/deploy.sh nginx` | 仅更新 Nginx 配置 |
| `sudo bash deploy/baota-deploy.sh` | 宝塔环境完整部署（含更多选项） |
| `sudo bash deploy/baota-deploy.sh --seed` | 完整部署 + 初始化种子数据 |
