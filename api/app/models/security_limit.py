from datetime import datetime

from sqlalchemy import String, SmallInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SecurityLimit(Base):
    __tablename__ = "security_limits"

    limit_type: Mapped[str] = mapped_column(String(50), primary_key=True)
    identifier: Mapped[str] = mapped_column(String(255), primary_key=True)
    fail_count: Mapped[int] = mapped_column(SmallInteger, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime)
    last_fail_at: Mapped[datetime | None] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
