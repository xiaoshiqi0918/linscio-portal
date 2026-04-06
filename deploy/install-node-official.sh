#!/usr/bin/env bash
#
# 备选：面板或软件商店无法安装 Node 18+ 时使用。从 nodejs.org 安装官方 Node 20 LTS 二进制到
# /www/server/nodejs/v<版本>/ ，与面板原有目录并列，便于 baota-deploy.sh 自动发现。
#
# 用法（root）：
#   sudo ./install-node-official.sh
#   sudo NODE_OFFICIAL_VERSION=22.14.0 ./install-node-official.sh
#   sudo NODEJS_INSTALL_ROOT=/opt/nodejs ./install-node-official.sh   # 自定义根目录（非宝塔路径）
#
# 装完后部署：
#   sudo LINSCIO_NODE_BIN=/www/server/nodejs/v20.18.3/bin /www/wwwroot/linscio-portal/deploy/baota-deploy.sh
# （具体版本号以脚本输出为准）
#
set -euo pipefail

DEFAULT_NODE_VER="20.18.3"
NODE_OFFICIAL_VERSION="${NODE_OFFICIAL_VERSION:-$DEFAULT_NODE_VER}"
NODEJS_INSTALL_ROOT="${NODEJS_INSTALL_ROOT:-/www/server/nodejs}"
LOG_PREFIX="[install-node-official]"

log()  { echo "$LOG_PREFIX $*"; }
fail() { echo "$LOG_PREFIX ERROR: $*" >&2; exit 1; }

if [[ "$(id -u)" -ne 0 ]]; then
  fail "请使用 root：sudo $0"
fi

case "$(uname -m)" in
  x86_64)  NODE_ARCH="linux-x64" ;;
  aarch64) NODE_ARCH="linux-arm64" ;;
  *) fail "不支持的架构：$(uname -m)，请从 https://nodejs.org 手动下载对应包" ;;
esac

VER="$NODE_OFFICIAL_VERSION"
VER="${VER#v}"
DEST="${NODEJS_INSTALL_ROOT}/v${VER}"
TARBALL="node-v${VER}-${NODE_ARCH}.tar.xz"
URL="https://nodejs.org/dist/v${VER}/${TARBALL}"
TMPDIR="${TMPDIR:-/tmp}"
WORK="$TMPDIR/linscio-node-install-$$"

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  sed -n '2,/^set -euo/p' "$0" | grep '^#' | grep -v '^#!' | head -n 22
  exit 0
fi

if [[ -x "${DEST}/bin/node" ]]; then
  if [[ "${FORCE_REINSTALL:-0}" != "1" ]]; then
    log "已存在 ${DEST}/bin/node ，跳过下载。若要重装：FORCE_REINSTALL=1 sudo $0"
    log "部署时请使用：LINSCIO_NODE_BIN=${DEST}/bin"
    exit 0
  fi
  log "FORCE_REINSTALL=1 ，将删除旧目录并重装"
  rm -rf "${DEST:?}"
fi

mkdir -p "$NODEJS_INSTALL_ROOT" "$WORK"
cd "$WORK"

if command -v curl &>/dev/null; then
  log "下载：$URL"
  curl -fSL -o "$TARBALL" "$URL"
elif command -v wget &>/dev/null; then
  log "下载：$URL"
  wget -q --show-progress -O "$TARBALL" "$URL"
else
  fail "需要 curl 或 wget"
fi

log "解压..."
tar -xf "$TARBALL"
EXTRACTED="node-v${VER}-${NODE_ARCH}"
[[ -d "$EXTRACTED" ]] || fail "解压后未找到目录 $EXTRACTED"

mkdir -p "$NODEJS_INSTALL_ROOT"
mv "$EXTRACTED" "$DEST"
rm -f "$TARBALL"
cd / && rmdir "$WORK" 2>/dev/null || rm -rf "$WORK"

chmod -R a+rX "$DEST" 2>/dev/null || true

NODE_BIN="${DEST}/bin/node"
NPM_BIN="${DEST}/bin/npm"
[[ -x "$NODE_BIN" ]] || fail "安装异常：缺少 $NODE_BIN"
[[ -x "$NPM_BIN" ]] || fail "安装异常：缺少 $NPM_BIN"

log "安装完成：$("$NODE_BIN" -v) / $("$NPM_BIN" -v)"
log "部署 linscio-portal 时使用："
log "  sudo LINSCIO_NODE_BIN=${DEST}/bin /www/wwwroot/linscio-portal/deploy/baota-deploy.sh"
log "或在面板「计划任务 / SSH」中把上述 LINSCIO_NODE_BIN 写进环境。"
