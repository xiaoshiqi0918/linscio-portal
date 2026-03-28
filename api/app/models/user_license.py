from datetime import datetime

from sqlalchemy import (
    BigInteger, String, SmallInteger, DateTime, Index,
    UniqueConstraint, JSON, ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, BigIntPK


class UserLicense(Base):
    __tablename__ = "user_licenses"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(String(50), ForeignKey("products.product_id"), nullable=False)
    is_trial: Mapped[int] = mapped_column(SmallInteger, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    device_fingerprint: Mapped[str | None] = mapped_column(String(128))
    device_name: Mapped[str | None] = mapped_column(String(255))
    access_token: Mapped[str | None] = mapped_column(String(128), unique=True)
    token_created_at: Mapped[datetime | None] = mapped_column(DateTime)
    rebind_count: Mapped[int] = mapped_column(SmallInteger, default=0)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime)
    last_seen_ip: Mapped[str | None] = mapped_column(String(45))
    reported_specialties: Mapped[dict | None] = mapped_column(JSON)
    reported_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_user_product"),
        Index("idx_access_token", "access_token"),
        Index("idx_license_expires_at", "expires_at"),
    )
