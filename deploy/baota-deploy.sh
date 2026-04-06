#!/usr/bin/env bash
#
# =============================================================================
# LinScio Portal — 宝塔环境「完整项目」一键部署脚本
# =============================================================================
#
# 覆盖范围（一次跑通整站交付物）：
#   ① 可选：从 linscio-portal.zip 解压到指定目录
#   ② 可选：从文件复制 api/.env（实现单次命令完成，无需脚本跑两次）
#   ③ Python venv、依赖、Alembic 迁移、可选 seed
#   ④ 四个前端 npm ci + vite build，静态资源同步到 LINSCIO_DEPLOY_ROOT
#   ⑤ 写入宝塔 Supervisor 子配置并尝试启动 linscio-api
#   ⑥ 生成 Nginx 参考配置（站点 root / 反代片段），便于粘贴到宝塔「网站 → 配置」
#
# 仍须在宝塔中手动完成（面板无通用 API）：
#   · 安装软件：Nginx、MySQL、Supervisor、Node 18+（面板；装不了 18+ 时备选 deploy/install-node-official.sh）
#   · 创建数据库与用户，并在 .env 中填写连接信息
#   · 为各域名添加网站、SSL；可将生成的参考配置中的 location 合并进站点
#
# 用法示例
# --------
#  0) 推荐：整仓放在宝塔 www 根下 /www/wwwroot/linscio-portal，无需设置 LINSCIO_PORTAL：
#     sudo /www/wwwroot/linscio-portal/deploy/baota-deploy.sh
#     sudo /www/wwwroot/linscio-portal/deploy/baota-deploy.sh --seed
#     （未设置 LINSCIO_PORTAL 时，自动依次尝试：脚本上级 → /www/wwwroot/linscio-portal → /home/linscio-portal → $HOME/linscio-portal）
#     静态输出默认在 /www/wwwroot/linscio-release/{www,portal,...}，与「网站目录」同盘，避免误用 wwwroot 默认页。
#
#  1) 项目或发布目录不在默认路径时再显式指定：
#     sudo LINSCIO_PORTAL=/其它路径/linscio-portal LINSCIO_DEPLOY_ROOT=/其它路径/linscio-release ./baota-deploy.sh
#
#  2) 从 zip 一键（zip 内根目录须为 linscio-portal/；解压父目录为 LINSCIO_PORTAL 的上一级）：
#     sudo LINSCIO_PORTAL=/www/wwwroot/linscio-portal LINSCIO_DEPLOY_ROOT=/www/wwwroot/linscio-release \
#       ./baota-deploy.sh --from-zip /root/linscio-portal.zip
#
#  3) 单次完成（已准备好 .env 文件，含数据库密码等）：
#     sudo LINSCIO_PORTAL=/www/wwwroot/linscio-portal LINSCIO_DEPLOY_ROOT=/www/wwwroot/linscio-release \
#       ./baota-deploy.sh --from-zip /root/linscio-portal.zip --env-file /root/linscio.env --seed
#
# 参数
# ----
#   --from-zip PATH     解压 zip 后再执行后续步骤（解压到 dirname(LINSCIO_PORTAL)，得到 LINSCIO_PORTAL）
#   --env-file PATH     部署前复制为 api/.env（覆盖已存在文件）
#   --seed              执行 scripts/seed.py（建议仅首次建库）
#   --no-nginx-snippets 不生成 nginx 参考文件
#   --no-self-check      跳过脚本末尾的本机自检与排查提示
#   --skip-frontend / --skip-backend / --skip-supervisor
#   --help
#
# 环境变量
# --------
#   LINSCIO_PORTAL          项目根（未设置时自动探测，见上文「用法 0」）
#   LINSCIO_DEPLOY_ROOT     静态输出根目录（默认 /www/wwwroot/linscio-release）
#   LINSCIO_DOMAIN_BASE     生成 Nginx 时的主域，如 linscio.com.cn（默认 linscio.com.cn）
#   ADMIN_NGINX_ALLOW_IP    admin 站点 allow 的公网 IP（可逗号分隔多个，会生成多行 allow）
#   RUN_USER                运行 uvicorn（默认 www 若存在）
#   SUPERVISOR_PROFILE_DIR  宝塔 Supervisor profile 目录
#   LINSCIO_NODE_BIN        含 npm、npx 的目录（宝塔常见：/www/server/nodejs/v18.x.x/bin）
#   LINSCIO_NPM             npm 可执行文件完整路径（与 LINSCIO_NODE_BIN 二选一即可）
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 项目根：显式 LINSCIO_PORTAL > 脚本上级 > /www/wwwroot/linscio-portal > /home/linscio-portal > $HOME/linscio-portal
_resolve_portal_root() {
  local _parent
  _parent="$(cd "$SCRIPT_DIR/.." && pwd)"
  if [[ -n "${LINSCIO_PORTAL:-}" ]]; then
    [[ -d "$LINSCIO_PORTAL" ]] || {
      echo "[LinScio full-deploy] ERROR: LINSCIO_PORTAL 不是目录：$LINSCIO_PORTAL" >&2
      exit 1
    }
    cd "$LINSCIO_PORTAL" && pwd
    return
  fi
  if [[ -f "$_parent/api/requirements.txt" ]]; then
    echo "$_parent"
    return
  fi
  if [[ -f "/www/wwwroot/linscio-portal/api/requirements.txt" ]]; then
    echo "/www/wwwroot/linscio-portal"
    return
  fi
  if [[ -f "/home/linscio-portal/api/requirements.txt" ]]; then
    echo "/home/linscio-portal"
    return
  fi
  if [[ -n "${HOME:-}" && -f "${HOME}/linscio-portal/api/requirements.txt" ]]; then
    cd "${HOME}/linscio-portal" && pwd
    return
  fi
  echo "$_parent"
}
PORTAL_ROOT="$(_resolve_portal_root)"
DEPLOY_ROOT="${LINSCIO_DEPLOY_ROOT:-/www/wwwroot/linscio-release}"
DOMAIN_BASE="${LINSCIO_DOMAIN_BASE:-linscio.com.cn}"
SUPERVISOR_PROFILE_DIR="${SUPERVISOR_PROFILE_DIR:-/www/server/panel/plugin/supervisor/profile}"
ADMIN_ALLOW_IPS="${ADMIN_NGINX_ALLOW_IP:-127.0.0.1}"

ZIPFILE=""
LINSCIO_ENV_FILE=""
SKIP_FRONTEND=0
SKIP_BACKEND=0
SKIP_SUPERVISOR=0
DO_SEED=0
GENERATE_NGINX=1
DO_SELF_CHECK=1

log()  { echo "[LinScio full-deploy] $*"; }
fail() { echo "[LinScio full-deploy] ERROR: $*" >&2; exit 1; }

# sudo 时 PATH 常不含宝塔 Node；自动探测 /www/server/nodejs/v*/bin
# 若同时装有 Node 14 与 20，优先选 >=18（避免 PATH 里旧 npm 抢先于宝塔目录）
_linscio_find_npm() {
  local p
  if [[ -n "${LINSCIO_NPM:-}" ]]; then
    p="${LINSCIO_NPM}"
    [[ -x "$p" ]] || p="$(type -P "$LINSCIO_NPM" 2>/dev/null || true)"
    if [[ -n "$p" && -x "$p" ]]; then
      echo "$p"
      return 0
    fi
  fi
  if [[ -n "${LINSCIO_NODE_BIN:-}" ]]; then
    p="${LINSCIO_NODE_BIN%/}/npm"
    if [[ -x "$p" ]]; then
      echo "$p"
      return 0
    fi
  fi
  shopt -s nullglob
  local -a _bt=(/www/server/nodejs/v*/bin/npm)
  shopt -u nullglob
  if [[ ${#_bt[@]} -gt 0 ]]; then
    local -a _ok=()
    for p in "${_bt[@]}"; do
      [[ -x "${p%/npm}/node" ]] || continue
      local _mj
      _mj="$("${p%/npm}/node" -p "process.versions.node.split('.')[0]" 2>/dev/null || echo 0)"
      [[ "$_mj" -ge 18 ]] && _ok+=("$p")
    done
    if [[ ${#_ok[@]} -gt 0 ]]; then
      printf '%s\n' "${_ok[@]}" | sort -V | tail -n1
      return 0
    fi
  fi
  if command -v npm &>/dev/null; then
    command -v npm
    return 0
  fi
  if [[ ${#_bt[@]} -gt 0 ]]; then
    printf '%s\n' "${_bt[@]}" | sort -V | tail -n1
    return 0
  fi
  p="/www/server/nodejs/bin/npm"
  [[ -x "$p" ]] && { echo "$p"; return 0; }
  p="/usr/local/bin/npm"
  [[ -x "$p" ]] && { echo "$p"; return 0; }
  return 1
}

_linscio_http_get_ok() {
  local url="$1"
  if command -v curl &>/dev/null; then
    curl -sf --max-time 5 -o /dev/null "$url"
  elif command -v wget &>/dev/null; then
    wget -q --timeout=5 -O /dev/null "$url" 2>/dev/null
  else
    return 2
  fi
}

# Supervisor 刚 restart 时 Uvicorn 可能尚未 bind，避免误报 FAIL
_linscio_wait_health() {
  local url="$1"
  local i
  for i in 1 2 3 4 5 6 7 8 9 10; do
    if _linscio_http_get_ok "$url"; then
      return 0
    fi
    sleep 1
  done
  return 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --help|-h)
      sed -n '1,/@baota-deploy-help-boundary/p' "$0" | sed '$d' | grep '^#' | grep -v '^#!'
      exit 0
      ;;
    --seed) DO_SEED=1; shift ;;
    --skip-frontend) SKIP_FRONTEND=1; shift ;;
    --skip-backend) SKIP_BACKEND=1; shift ;;
    --skip-supervisor) SKIP_SUPERVISOR=1; shift ;;
    --no-nginx-snippets) GENERATE_NGINX=0; shift ;;
    --no-self-check) DO_SELF_CHECK=0; shift ;;
    --from-zip)
      [[ -n "${2:-}" ]] || fail "--from-zip 需要 zip 文件路径"
      ZIPFILE="$2"
      shift 2
      ;;
    --env-file)
      [[ -n "${2:-}" ]] || fail "--env-file 需要文件路径"
      LINSCIO_ENV_FILE="$2"
      shift 2
      ;;
    *)
      fail "未知参数: $1 （使用 --help）"
      ;;
  esac
done

# --from-zip 且未指定 LINSCIO_PORTAL：若当前探测结果还不是有效仓库根，固定为宝塔 www 下常见路径，
# 避免从 /tmp、/root 仅复制脚本执行时 dirname(PORTAL_ROOT) 变成 / 把 zip 解到系统根目录。
if [[ -n "$ZIPFILE" && -z "${LINSCIO_PORTAL:-}" ]]; then
  if [[ ! -f "$PORTAL_ROOT/api/requirements.txt" ]]; then
    PORTAL_ROOT="/www/wwwroot/linscio-portal"
  fi
fi

if [[ "$(id -u)" -ne 0 ]]; then
  fail "请使用 root：sudo $0 ..."
fi

if id -u www &>/dev/null; then
  RUN_USER="${RUN_USER:-www}"
else
  RUN_USER="${RUN_USER:-root}"
fi

# ---------- 解压 zip ----------
if [[ -n "$ZIPFILE" ]]; then
  [[ -f "$ZIPFILE" ]] || fail "找不到 zip：$ZIPFILE"
  command -v unzip &>/dev/null || fail "请先安装 unzip：apt install -y unzip"
  UNZIP_PARENT="$(dirname "$PORTAL_ROOT")"
  [[ "$UNZIP_PARENT" != "/" ]] || fail "解压父目录不能为 / ，请设置 LINSCIO_PORTAL=/www/wwwroot/linscio-portal（或实际项目路径）"
  mkdir -p "$UNZIP_PARENT"
  log "解压：$ZIPFILE → $UNZIP_PARENT"
  unzip -o -q "$ZIPFILE" -d "$UNZIP_PARENT"
  if [[ ! -d "$PORTAL_ROOT/api" ]]; then
    if [[ -d "$UNZIP_PARENT/linscio-portal/api" && "$PORTAL_ROOT" != "$UNZIP_PARENT/linscio-portal" ]]; then
      log "将 $UNZIP_PARENT/linscio-portal 移动到 $PORTAL_ROOT"
      mkdir -p "$(dirname "$PORTAL_ROOT")"
      rm -rf "$PORTAL_ROOT" 2>/dev/null || true
      mv "$UNZIP_PARENT/linscio-portal" "$PORTAL_ROOT"
    fi
  fi
fi

API_DIR="$PORTAL_ROOT/api"
VENV_DIR="$API_DIR/venv"
UVICORN_BIN="$VENV_DIR/bin/uvicorn"

if [[ -n "${LINSCIO_PORTAL:-}" ]]; then
  log "PORTAL_ROOT=$PORTAL_ROOT（LINSCIO_PORTAL）"
else
  log "PORTAL_ROOT=$PORTAL_ROOT（自动探测：脚本上级 → /www/wwwroot/linscio-portal → /home/linscio-portal → \$HOME/linscio-portal）"
fi
log "DEPLOY_ROOT=$DEPLOY_ROOT"
log "RUN_USER=$RUN_USER"

[[ -d "$API_DIR" ]] || fail "未找到项目 api：$API_DIR。请确认整仓在 /www/wwwroot/linscio-portal（或原 /home/linscio-portal），或设置 LINSCIO_PORTAL"
[[ -f "$API_DIR/requirements.txt" ]] || fail "未找到 $API_DIR/requirements.txt"

command -v python3 &>/dev/null || fail "未找到 python3"

if [[ "$SKIP_FRONTEND" -eq 0 ]]; then
  NPM_PATH="$(_linscio_find_npm)" || fail "未找到 npm。
  原因多为：用 sudo 执行时 PATH 不含宝塔 Node（面板「Node 版本管理器」装在 /www/server/nodejs/v版本号/bin）。
  在服务器上可先执行：ls /www/server/nodejs/v*/bin/npm
  再任选其一：
    sudo LINSCIO_NODE_BIN=/www/server/nodejs/v18.20.0/bin $0 ...
  或：
    sudo LINSCIO_NPM=/www/server/nodejs/v18.20.0/bin/npm $0 ...
  NVM 用户请填对应 versions/node/.../bin/npm 。"
  export PATH="$(dirname "$NPM_PATH"):$PATH"
  log "npm：$NPM_PATH（已加入 PATH 前缀供 npx 使用）"
  NODE_BIN="$(dirname "$NPM_PATH")/node"
  [[ -x "$NODE_BIN" ]] || fail "未找到与 npm 同目录的 node：$NODE_BIN"
  _NODE_MAJ="$("$NODE_BIN" -p "process.versions.node.split('.')[0]" 2>/dev/null || echo 0)"
  if [[ "$_NODE_MAJ" -lt 18 ]]; then
    fail "当前 Node $($NODE_BIN -v) 过旧（需 >= 18）。package-lock.json 为 lockfileVersion 3，Vite 5 需 Node 18+。
请在宝塔「Node 版本管理器」安装 **18 或 20**，并确认服务器上存在：ls /www/server/nodejs/v*/bin/npm
然后指定高版本目录，例如：sudo LINSCIO_NODE_BIN=/www/server/nodejs/v20.x.x/bin $0 ...
若面板列表里**没有** 18/20，可备选：sudo bash $SCRIPT_DIR/install-node-official.sh"
  fi
  log "Node：$("$NODE_BIN" -v)（满足 >=18）"
fi

# ---------- 预置 .env ----------
if [[ -n "$LINSCIO_ENV_FILE" ]]; then
  [[ -f "$LINSCIO_ENV_FILE" ]] || fail "找不到 --env-file：$LINSCIO_ENV_FILE"
  install -m 640 -o "$RUN_USER" -g "$RUN_USER" "$LINSCIO_ENV_FILE" "$API_DIR/.env" 2>/dev/null || \
    cp "$LINSCIO_ENV_FILE" "$API_DIR/.env" && chmod 640 "$API_DIR/.env"
  chown "$RUN_USER:$RUN_USER" "$API_DIR/.env" 2>/dev/null || true
  log "已复制环境文件 → $API_DIR/.env"
fi

mkdir -p "$DEPLOY_ROOT"/{www,medcomm,portal,admin,logs}

if [[ ! -f "$API_DIR/.env" ]]; then
  if [[ -f "$API_DIR/.env.production.example" ]]; then
    cp "$API_DIR/.env.production.example" "$API_DIR/.env"
    chmod 640 "$API_DIR/.env"
    chown "$RUN_USER:$RUN_USER" "$API_DIR/.env" 2>/dev/null || true
    fail "已创建 $API_DIR/.env 。请填写 MySQL 等后重跑，或使用：$0 --env-file /path/to/your.env ..."
  else
    fail "缺少 $API_DIR/.env ，且无 .env.production.example"
  fi
fi

chown "$RUN_USER:$RUN_USER" "$API_DIR/.env" 2>/dev/null || true
chmod 640 "$API_DIR/.env" 2>/dev/null || true

# ---------- Python ----------
if [[ "$SKIP_BACKEND" -eq 0 ]]; then
  log "Python venv + pip ..."
  if [[ ! -d "$VENV_DIR" ]]; then
    python3 -m venv "$VENV_DIR"
  fi
  "$VENV_DIR/bin/pip" install -U pip -q
  "$VENV_DIR/bin/pip" install -r "$API_DIR/requirements.txt" -q
  chown -R "$RUN_USER:$RUN_USER" "$VENV_DIR" 2>/dev/null || true

  log "alembic upgrade head"
  ( cd "$API_DIR" && env PYTHONPATH=. "$VENV_DIR/bin/python" -m alembic upgrade head ) \
    || fail "数据库迁移失败，请检查 .env 中 MySQL"

  if [[ "$DO_SEED" -eq 1 ]]; then
    log "seed.py"
    ( cd "$API_DIR" && env PYTHONPATH=. "$VENV_DIR/bin/python" scripts/seed.py ) || true
  fi
else
  log "已跳过 --skip-backend"
fi

# ---------- 前端 ----------
if [[ "$SKIP_FRONTEND" -eq 0 ]]; then
  for site in www medcomm-site portal admin; do
    log "前端构建：$site"
    pushd "$PORTAL_ROOT/$site" >/dev/null
    npm ci --no-fund --no-audit
    npx vite build
    popd >/dev/null
  done
  log "同步静态资源 → $DEPLOY_ROOT"
  rm -rf "${DEPLOY_ROOT:?}/www"/* "${DEPLOY_ROOT}/medcomm"/* "${DEPLOY_ROOT}/portal"/* "${DEPLOY_ROOT}/admin"/*
  cp -a "$PORTAL_ROOT/www/dist/." "$DEPLOY_ROOT/www/"
  cp -a "$PORTAL_ROOT/medcomm-site/dist/." "$DEPLOY_ROOT/medcomm/"
  cp -a "$PORTAL_ROOT/portal/dist/." "$DEPLOY_ROOT/portal/"
  cp -a "$PORTAL_ROOT/admin/dist/." "$DEPLOY_ROOT/admin/"
  chown -R "$RUN_USER:$RUN_USER" "$DEPLOY_ROOT/www" "$DEPLOY_ROOT/medcomm" "$DEPLOY_ROOT/portal" "$DEPLOY_ROOT/admin" "$DEPLOY_ROOT/logs"
else
  log "已跳过 --skip-frontend"
fi

# ---------- Supervisor ----------
if [[ "$SKIP_SUPERVISOR" -eq 0 ]]; then
  if [[ ! -d "$SUPERVISOR_PROFILE_DIR" ]]; then
    log "未找到 $SUPERVISOR_PROFILE_DIR ，跳过 Supervisor"
  else
    SUP_INI="$SUPERVISOR_PROFILE_DIR/linscio-api.ini"
    log "写入 $SUP_INI"
    cat >"$SUP_INI" <<EOF
[program:linscio-api]
command=$UVICORN_BIN app.main:app --host 127.0.0.1 --port 8000 --workers 2
directory=$API_DIR
user=$RUN_USER
autostart=true
autorestart=true
startretries=3
stdout_logfile=$DEPLOY_ROOT/logs/api.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
stderr_logfile=$DEPLOY_ROOT/logs/api_error.log
environment=ENV="production"
EOF
    if command -v supervisorctl &>/dev/null; then
      supervisorctl reread 2>/dev/null || true
      supervisorctl update linscio-api 2>/dev/null || supervisorctl update 2>/dev/null || true
      supervisorctl restart linscio-api 2>/dev/null || supervisorctl start linscio-api 2>/dev/null || \
        log "请在宝塔 Supervisor 中重载并启动 linscio-api"
    else
      log "未找到 supervisorctl，请在宝塔中重载 Supervisor"
    fi
  fi
else
  log "已跳过 --skip-supervisor"
fi

# @baota-deploy-help-boundary（--help 只打印本行之前的 # 注释，勿删）
# ---------- Nginx 参考（完整五站 + 反代规则）----------
if [[ "$GENERATE_NGINX" -eq 1 ]]; then
  NG_OUT="$DEPLOY_ROOT/nginx-linscio-full-reference.conf"
  log "生成 Nginx 参考：$NG_OUT"
  WWW_SN="$DOMAIN_BASE"
  MED_SN="medcomm.$DOMAIN_BASE"
  POR_SN="portal.$DOMAIN_BASE"
  ADM_SN="admin.$DOMAIN_BASE"
  API_SN="api.$DOMAIN_BASE"

  ALLOW_BLOCK=""
  IFS=',' read -ra _IPS <<< "$ADMIN_ALLOW_IPS"
  for ip in "${_IPS[@]}"; do
    ip="$(echo "$ip" | xargs)"
    [[ -n "$ip" ]] || continue
    ALLOW_BLOCK+="    allow $ip;"$'\n'
  done
  [[ -n "$ALLOW_BLOCK" ]] || ALLOW_BLOCK="    allow 127.0.0.1;"$'\n'

  cat >"$NG_OUT" <<NGEOF
# =============================================================================
# LinScio Portal — 完整 Nginx 参考（由 baota-deploy.sh 生成）
# 域名基：$DOMAIN_BASE
# 静态根：$DEPLOY_ROOT
#
# 使用方式（宝塔）：
#   1. 为 www / medcomm / portal / admin / api 分别「添加站点」
#   2. 网站目录分别设为：$DEPLOY_ROOT/www、medcomm、portal、admin；api 可任意空目录
#   3. 打开站点「配置文件」，将下面对应 server { } 中 location 与 root 合并进去
#      （宝塔已生成 listen/ssl 时不要重复 listen 443，只合并 root 与 location）
#   4. 在面板申请 SSL 并强制 HTTPS
#   5. admin 的 allow 须与 api/.env 中 ADMIN_IPS 一致；可设置环境变量 ADMIN_NGINX_ALLOW_IP=1.2.3.4,5.6.7.8 后重跑脚本重新生成
#   6. location /api/ 中 proxy_pass 须为 http://127.0.0.1:8000 （末尾无 /），否则路径被改写，POST 注册/登录易变 405 Method Not Allowed
# =============================================================================

# --- www ---
server {
    listen 80;
    server_name $WWW_SN;
    root $DEPLOY_ROOT/www;
    index index.html;
    location / {
        try_files \$uri \$uri/ /index.html;
    }
}

# --- medcomm ---
server {
    listen 80;
    server_name $MED_SN;
    root $DEPLOY_ROOT/medcomm;
    index index.html;
    location / {
        try_files \$uri \$uri/ /index.html;
    }
}

# --- portal ---
server {
    listen 80;
    server_name $POR_SN;
    root $DEPLOY_ROOT/portal;
    index index.html;
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Connection        "";
        proxy_connect_timeout 10s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
    location / {
        try_files \$uri \$uri/ /index.html;
    }
}

# --- admin ---
server {
    listen 80;
    server_name $ADM_SN;
$ALLOW_BLOCK    deny all;
    root $DEPLOY_ROOT/admin;
    index index.html;
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Connection        "";
        proxy_connect_timeout 10s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Connection        "";
        proxy_connect_timeout 10s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
    location / {
        try_files \$uri \$uri/ /index.html;
    }
}

# --- api（整站反代）---
server {
    listen 80;
    server_name $API_SN;
    client_max_body_size 10m;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Connection        "";
        proxy_connect_timeout 10s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
}
NGEOF
  chmod 644 "$NG_OUT"
  log "请打开 $NG_OUT 按说明合并到宝塔各站点"
fi

log "======== 完整部署流程结束 ========"

if [[ "$DO_SELF_CHECK" -eq 1 ]]; then
  log "---------- 本机自检（脚本只验证本机服务，不验证域名）----------"
  if [[ "$SKIP_BACKEND" -eq 0 ]]; then
    if _linscio_wait_health "http://127.0.0.1:8000/health"; then
      log "OK  API 本机可访问：curl -s http://127.0.0.1:8000/health"
    else
      log "FAIL 本机 8000 无响应（已重试约 10s）。请执行：supervisorctl status linscio-api"
      log "     查看日志：tail -80 $DEPLOY_ROOT/logs/api_error.log"
      log "     手工试跑：sudo -u $RUN_USER bash -c 'cd $API_DIR && env PYTHONPATH=. $VENV_DIR/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000'"
    fi
  else
    log "（已 --skip-backend，跳过 API 自检）"
  fi
  if [[ "$SKIP_FRONTEND" -eq 0 ]]; then
    if [[ -f "$DEPLOY_ROOT/www/index.html" && -f "$DEPLOY_ROOT/portal/index.html" ]]; then
      log "OK  静态文件存在：$DEPLOY_ROOT/www/index.html 与 portal/index.html"
    else
      log "FAIL 静态目录不完整，请检查 $DEPLOY_ROOT 下是否含各站 dist"
    fi
  else
    log "（已 --skip-frontend，跳过静态自检）"
  fi
  if command -v ss &>/dev/null && ss -tln 2>/dev/null | grep -qE ':(80|443)\b'; then
    log "OK  本机正在监听 80 或 443（Nginx 可能已运行）"
  else
    log "提示 未检测到 80/443 监听，外网用 http(s)://域名 访问会失败；请启动 Nginx 并放行端口"
  fi
  log "---------- 浏览器仍打不开站点时，请核对 ----------"
  log "1) 宝塔「网站」里该域名的 网站目录 是否指向 $DEPLOY_ROOT 下对应子目录"
  log "   例：www 站点 → $DEPLOY_ROOT/www ，portal → $DEPLOY_ROOT/portal（勿指到源码里的 www/ 应用目录）"
  log "2) 是否已将 $DEPLOY_ROOT/nginx-linscio-full-reference.conf 中的 root 与 /api/ 反代合并进站点配置"
  log "3) 云服务器安全组 + 宝塔「安全」是否放行 80、443"
  log "4) 域名 DNS 的 A 记录是否指向本机公网 IP"
  log "5) SSH 执行 curl -sI http://你的域名/ 或 curl -sI -H 'Host: 你的域名' http://127.0.0.1/ 看是否 200/301"
fi

log "健康检查：curl -s http://127.0.0.1:8000/health"
log "补跑 seed：cd $API_DIR && source venv/bin/activate && PYTHONPATH=. python scripts/seed.py"
