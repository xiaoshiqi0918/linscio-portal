from datetime import datetime

from sqlalchemy import BigInteger, String, SmallInteger, Text, DateTime, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, BigIntPK


class DownloadLog(Base):
    __tablename__ = "download_logs"

    id: Mapped[int] = mapped_column(BigIntPK, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    download_type: Mapped[str] = mapped_column(String(20), nullable=False)  # 'software' | 'specialty' | 'drawing_pack' | 'bundle'
    resource_id: Mapped[str | None] = mapped_column(String(100))
    platform: Mapped[str | None] = mapped_column(String(30))
    client_ip: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(Text)
    completed: Mapped[int] = mapped_column(SmallInteger, default=0)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_dl_user_created", "user_id", "created_at"),
        Index("idx_dl_type_created", "download_type", "created_at"),
    )
