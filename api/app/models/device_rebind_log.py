from datetime import datetime

from sqlalchemy import BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, BigIntPK


class DeviceRebindLog(Base):
    __tablename__ = "device_rebind_logs"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(String(50), nullable=False)
    old_fingerprint: Mapped[str | None] = mapped_column(String(128))
    new_fingerprint: Mapped[str | None] = mapped_column(String(128))
    old_device_name: Mapped[str | None] = mapped_column(String(255))
    new_device_name: Mapped[str | None] = mapped_column(String(255))
    rebind_type: Mapped[str | None] = mapped_column(String(20))  # 'self_service' | 'admin'
    operator_ip: Mapped[str | None] = mapped_column(String(45))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
