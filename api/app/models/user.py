from datetime import datetime

from sqlalchemy import BigInteger, String, SmallInteger, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, BigIntPK


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[int] = mapped_column(SmallInteger, default=1)
    is_admin: Mapped[int] = mapped_column(SmallInteger, default=0)
    email_verified: Mapped[int] = mapped_column(SmallInteger, default=0)
    email_notified_7d: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=datetime.utcnow)

    __table_args__ = (Index("idx_email", "email"),)
