#!/usr/bin/env python3
"""
本地冒烟：验证注册与管理端 API（需已配置 api/.env，且 SQLite/MySQL 可用）。

用法（在 api 目录）:
  PYTHONPATH=. python scripts/smoke_local.py
"""
from __future__ import annotations

import logging
import os
import sys
import uuid

# 减少 SQL 日志刷屏
logging.basicConfig(level=logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

os.chdir(_root)

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


def main() -> int:
    client = TestClient(app)

    r = client.get("/health")
    assert r.status_code == 200, r.text
    print("OK  GET /health")

    email = f"smoke_{uuid.uuid4().hex[:10]}@example.com"
    r = client.post("/api/auth/register", json={"email": email, "password": "SmokeTest1!"})
    assert r.status_code == 200, f"register: {r.status_code} {r.text}"
    body = r.json()
    assert body.get("success") is True, body
    print(f"OK  POST /api/auth/register  ({email})")

    r = client.post(
        "/api/auth/login",
        json={"email": "admin@linscio.com.cn", "password": "admin123456"},
    )
    if r.status_code != 200:
        print(
            "FAIL POST /api/auth/login — 请先执行: PYTHONPATH=. python scripts/seed.py",
            file=sys.stderr,
        )
        print(r.status_code, r.text, file=sys.stderr)
        return 1
    token = r.json()["session_token"]
    h = {"Authorization": f"Bearer {token}"}
    print("OK  POST /api/auth/login (admin)")

    for path in (
        "/admin/stats/overview",
        "/admin/users?page=1&size=5",
        "/admin/logs/admin?page=1&size=5",
    ):
        r = client.get(path, headers=h)
        assert r.status_code == 200, f"{path}: {r.status_code} {r.text}"
        print(f"OK  GET {path.split('?')[0]}")

    print("\n全部通过。本地后端逻辑正常。")
    print("若线上仍 502：查 Nginx 反代与超时；若管理端 403：查 .env ADMIN_IPS 与 X-Forwarded-For。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
