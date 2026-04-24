from sqlalchemy import String, Boolean, DateTime, func, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.user import User 

class AuthIdentity(Base):
    __tablename__ = "auth_identities"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    provider_uid: Mapped[str] = mapped_column(String(255), nullable=False)
    provider_email: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        UniqueConstraint("provider", "provider_uid", name="uq_provider_uid"),
    )
    
    user: Mapped["User"] = relationship(back_populates="auth_identities")
