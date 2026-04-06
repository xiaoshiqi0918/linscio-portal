#!/usr/bin/env bash
set -euo pipefail

#
# LinScio Portal — One-click deployment script
# Usage: ./deploy.sh [all|frontend|backend|migrate|nginx]
#
# 默认：源码 /www/wwwroot/linscio-portal，静态发布 /www/wwwroot/linscio-release（与 baota-deploy.sh 一致）
# 可覆盖：REPO_DIR=... RELEASE_ROOT=... ./deploy.sh frontend

REPO_DIR="${REPO_DIR:-/www/wwwroot/linscio-portal}"
RELEASE_ROOT="${RELEASE_ROOT:-/www/wwwroot/linscio-release}"
VENV_DIR="$REPO_DIR/api/venv"
LOG_PREFIX="[LinScio Deploy]"

log()  { echo "$LOG_PREFIX $*"; }
fail() { echo "$LOG_PREFIX ERROR: $*" >&2; exit 1; }

# ---------- Frontend build & deploy ----------
deploy_frontend() {
    log "Building and deploying frontend projects..."

    for site in www medcomm-site portal admin; do
        log "  Building $site..."
        cd "$REPO_DIR/$site"
        npm ci --production=false
        npx vite build

        case "$site" in
            www)           target="$RELEASE_ROOT/www" ;;
            medcomm-site)  target="$RELEASE_ROOT/medcomm" ;;
            portal)        target="$RELEASE_ROOT/portal" ;;
            admin)         target="$RELEASE_ROOT/admin" ;;
        esac

        mkdir -p "$target"
        rm -rf "${target:?}/"*
        cp -a dist/. "$target/"
        log "  $site → $target ✓"
    done

    log "Frontend deploy complete."
}

# ---------- Backend deploy ----------
deploy_backend() {
    log "Deploying backend..."

    cd "$REPO_DIR/api"

    if [ ! -d "$VENV_DIR" ]; then
        log "  Creating virtualenv..."
        python3 -m venv "$VENV_DIR"
    fi

    source "$VENV_DIR/bin/activate"
    pip install -r requirements.txt --quiet

    log "  Restarting linscio-api via supervisor..."
    supervisorctl restart linscio-api

    log "Backend deploy complete."
}

# ---------- Database migration ----------
deploy_migrate() {
    log "Running database migrations..."

    cd "$REPO_DIR/api"
    source "$VENV_DIR/bin/activate"
    PYTHONPATH=. alembic upgrade head

    log "Migration complete."
}

# ---------- Nginx config ----------
deploy_nginx() {
    log "Deploying nginx configs..."

    NGINX_CONF_DIR="${NGINX_CONF_DIR:-/www/server/panel/vhost/nginx}"
    DEPLOY_NGINX_DIR="$REPO_DIR/deploy/nginx"

    for conf in "$DEPLOY_NGINX_DIR"/*.conf; do
        filename=$(basename "$conf")
        cp "$conf" "$NGINX_CONF_DIR/$filename"
        log "  $filename → $NGINX_CONF_DIR/ ✓"
    done

    nginx -t || fail "Nginx config test failed!"
    systemctl reload nginx

    log "Nginx deploy complete."
}

# ---------- Main ----------
ACTION="${1:-all}"

case "$ACTION" in
    frontend) deploy_frontend ;;
    backend)  deploy_backend ;;
    migrate)  deploy_migrate ;;
    nginx)    deploy_nginx ;;
    all)
        deploy_frontend
        deploy_migrate
        deploy_backend
        deploy_nginx
        log "=== Full deployment complete ==="
        ;;
    *)
        echo "Usage: $0 [all|frontend|backend|migrate|nginx]"
        exit 1
        ;;
esac
