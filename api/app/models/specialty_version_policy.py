from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SpecialtyVersionPolicy(Base):
    __tablename__ = "specialty_version_policy"

    specialty_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    product_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("products.product_id"), primary_key=True
    )
    force_min_version: Mapped[str | None] = mapped_column(String(20))
    force_max_version: Mapped[str | None] = mapped_column(String(20))
    policy_message: Mapped[str | None] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
