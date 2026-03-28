from datetime import datetime

from sqlalchemy import BigInteger, String, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, BigIntPK


class UserSpecialty(Base):
    __tablename__ = "user_specialties"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(String(50), ForeignKey("products.product_id"), nullable=False)
    specialty_id: Mapped[str] = mapped_column(String(50), nullable=False)
    license_code_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("license_codes.id"))
    purchased_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", "specialty_id", name="uq_user_product_specialty"),
    )
