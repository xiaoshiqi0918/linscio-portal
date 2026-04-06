"""admin_logs_created_at_index

Revision ID: c1a2b3c4d5e6
Revises: fd3929d0f150
Create Date: 2026-03-29

列表按 created_at 排序时走索引，避免大表全表扫描导致接口超时、Nginx 502。
"""
from typing import Sequence, Union

from alembic import op


revision: str = "c1a2b3c4d5e6"
down_revision: Union[str, None] = "fd3929d0f150"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("admin_logs", schema=None) as batch_op:
        batch_op.create_index(
            "idx_admin_log_created_at", ["created_at"], unique=False
        )


def downgrade() -> None:
    with op.batch_alter_table("admin_logs", schema=None) as batch_op:
        batch_op.drop_index("idx_admin_log_created_at")
