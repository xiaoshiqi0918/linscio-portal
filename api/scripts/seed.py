"""
Seed script — initializes products and admin user for local development.

Usage:
    cd api && source venv/bin/activate
    PYTHONPATH=. python scripts/seed.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime

from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models.product import Product
from app.models.user import User

PRODUCTS = [
    {
        "product_id": "medcomm",
        "name": "LinScio MedComm",
        "description": "AI 医学翻译与沟通工具，支持 LangGraph 多轮对话",
        "sort_order": 1,
    },
    {
        "product_id": "schola",
        "name": "LinScio Schola",
        "description": "学术文献阅读与知识管理平台",
        "sort_order": 2,
    },
]

ADMIN_EMAIL = "admin@linscio.com.cn"
ADMIN_PASSWORD = "admin123456"


def seed():
    db = SessionLocal()
    try:
        created = []

        for p in PRODUCTS:
            existing = db.query(Product).filter_by(product_id=p["product_id"]).first()
            if existing:
                print(f"  [skip] Product '{p['product_id']}' already exists")
            else:
                db.add(Product(**p))
                created.append(f"Product '{p['product_id']}'")

        admin = db.query(User).filter_by(email=ADMIN_EMAIL).first()
        if admin:
            print(f"  [skip] Admin '{ADMIN_EMAIL}' already exists")
        else:
            db.add(
                User(
                    email=ADMIN_EMAIL,
                    password_hash=hash_password(ADMIN_PASSWORD),
                    is_active=1,
                    is_admin=1,
                    email_verified=1,
                    created_at=datetime.utcnow(),
                )
            )
            created.append(f"Admin '{ADMIN_EMAIL}'")

        db.commit()

        if created:
            print(f"\n  Seeded {len(created)} records:")
            for c in created:
                print(f"    + {c}")
        else:
            print("\n  Nothing to seed — all records already exist.")

        print(f"\n  Admin login:  {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
        print("  (Change this password after first login in production!)\n")

    finally:
        db.close()


if __name__ == "__main__":
    print("\n=== LinScio Portal — Seed Data ===\n")
    seed()
    print("=== Done ===\n")
