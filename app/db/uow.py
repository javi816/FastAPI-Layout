from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.modules.auth.repository import AuthIdentityRepository
from app.modules.user.repository import UserRepository, RoleRepository, UserRoleRepository



class UnitOfWork:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session = self._session_factory()
        self.user_repository = UserRepository(self.session)
        self.role_repository = RoleRepository(self.session)
        self.user_role_repository = UserRoleRepository(self.session)
        self.auth_identity_repository = AuthIdentityRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()