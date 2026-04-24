from sqlalchemy import String, Boolean, DateTime, func, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING
from app.db.base import Base

if TYPE_CHECKING:
    from app.modules.auth import AuthIdentity

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    roles: Mapped[list["Role"]] = relationship(secondary="user_roles", back_populates="users", lazy="selectin", overlaps="user_roles")
    user_roles: Mapped[list["UserRole"]] = relationship(back_populates="user", cascade="all, delete-orphan", overlaps="roles,users")
    auth_identities: Mapped[list["AuthIdentity"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Role(Base):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    users: Mapped[list["User"]] = relationship(secondary="user_roles", back_populates="roles", overlaps="user_roles")
    user_roles: Mapped[list["UserRole"]] = relationship(back_populates="role", cascade="all, delete-orphan", overlaps="users,roles")


class UserRole(Base):
    __tablename__ = "user_roles"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(),nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    user: Mapped["User"] = relationship(back_populates="user_roles", overlaps="roles,users")
    role: Mapped["Role"] = relationship(back_populates="user_roles", overlaps="roles,users")