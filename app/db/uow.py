from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.repository import AuthIdentityRepository
from app.modules.user.repository import UserRepository, RoleRepository, UserRoleRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        
        #Repos
        self.user_repository = UserRepository(session)
        self.role_repository = RoleRepository(session)
        self.user_role_repository = UserRoleRepository(session)
        self.auth_identity_repository = AuthIdentityRepository(session)
    
    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()