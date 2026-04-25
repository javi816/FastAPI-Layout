from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .model import AuthIdentity
from app.modules.user.model import User

class AuthIdentityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_provider_uid(self, provider: str, provider_uid: str) -> User | None:
        stmt = (
            select(User)
            .join(AuthIdentity, AuthIdentity.user_id == User.id)
            .options(selectinload(User.roles))
            .where(
                AuthIdentity.provider == provider,
                AuthIdentity.provider_uid == provider_uid,
                User.deleted_at.is_(None)
            )
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()