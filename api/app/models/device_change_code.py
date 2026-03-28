from datetime import datetime

from sqlalchemy import BigInteger, String, SmallInteger, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, BigIntPK


class DeviceChangeCode(Base):
    __tablename__ = "device_change_codes"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    product_id: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    new_fingerprint: Mapped[str] = mapped_column(String(128), nullable=False)
    new_device_name: Mapped[str | None] = mapped_column(String(255))
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_used: Mapped[int] = mapped_column(SmallInteger, default=0)
    fail_count: Mapped[int] = mapped_column(SmallInteger, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (Index("idx_dcc_user_product", "user_id", "product_id"),)
