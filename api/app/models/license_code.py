from datetime import datetime

from sqlalchemy import BigInteger, String, SmallInteger, Text, DateTime, Index, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, BigIntPK


class LicenseCode(Base):
    __tablename__ = "license_codes"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    product_id: Mapped[str] = mapped_column(String(50), ForeignKey("products.product_id"), nullable=False)
    license_type: Mapped[str] = mapped_column(String(20), nullable=False)  # 'basic' | 'specialty'
    duration_months: Mapped[int | None] = mapped_column(SmallInteger)
    is_trial: Mapped[int] = mapped_column(SmallInteger, default=0)
    specialty_ids: Mapped[dict | None] = mapped_column(JSON)
    is_activated: Mapped[int] = mapped_column(SmallInteger, default=0)
    activated_by: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.id"))
    activated_at: Mapped[datetime | None] = mapped_column(DateTime)
    recipient_note: Mapped[str | None] = mapped_column(Text)
    created_by_admin: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_license_code", "code"),
        Index("idx_license_product", "product_id"),
    )
