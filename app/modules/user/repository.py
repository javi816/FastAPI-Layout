from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


from .model import User, Role, UserRole

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, user_id: int, only_active: bool = True, include_deleted: bool = False) -> User | None:
        stmt = select(User).where(User.id == user_id)
        if not include_deleted:
            stmt = stmt.where(User.deleted_at.is_(None))
            
        if only_active:
            stmt = stmt.where(User.is_active.is_(True))
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
    
    async def get_by_email(self, user_email: str, only_active: bool = True, include_deleted: bool = False) -> User | None:
        stmt = select(User).where(User.email == user_email)
        if not include_deleted:
            stmt = stmt.where(User.deleted_at.is_(None))
        
        if only_active:
            stmt = stmt.where(User.is_active.is_(True))
            
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
    
    async def list_users(self, *, limit: int, offset: int, only_active: bool = True, include_deleted: bool = False) -> list[User]:
        stmt = select(User)
        if not include_deleted:
            stmt = stmt.where(User.deleted_at.is_(None))
        
        if only_active:
            stmt = stmt.where(User.is_active.is_(True))
        stmt = stmt.limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def count_users(self, *, only_active: bool = True, include_deleted: bool = False) -> int:
        stmt = select(func.count()).select_from(User)
        if not include_deleted:
            stmt = stmt.where(User.deleted_at.is_(None))
        
        if only_active:
            stmt = stmt.where(User.is_active.is_(True))
        
        result = await self.db.execute(stmt)
        return result.scalar_one()
    
    async def save(self, user: User) -> User:
        self.db.add(user)
        return user

    async def delete(self, user: User) -> None:
        await self.db.delete(user)


class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, role_id: int, include_deleted: bool = False) -> Role | None:
        
        stmt = select(Role).where(Role.id == role_id)
        
        if not include_deleted:
            stmt = stmt.where(Role.deleted_at.is_(None))
            
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
    
    async def list_roles(self, *, limit: int, offset: int, include_deleted: bool = False) -> list[Role]:
        
        stmt = select(Role)
        
        if not include_deleted:
            stmt = stmt.where(Role.deleted_at.is_(None))
        
        stmt = stmt.limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def count_roles(self, *, include_deleted: bool = False) -> int:
        
        stmt = select(func.count()).select_from(Role)
        
        if not include_deleted:
            stmt = stmt.where(Role.deleted_at.is_(None))
        
        result = await self.db.execute(stmt)
        return result.scalar_one()
    
    async def save(self, role: Role) -> Role:
        self.db.add(role)
        return role
    
    async def delete(self, role: Role) -> None:
        await self.db.delete(role)


class UserRoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_user_and_role(self, *, user_id: int, role_id: int, include_deleted: bool = False) -> UserRole | None:
        stmt = select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role_id)
        
        if not include_deleted:
            stmt = stmt.where(UserRole.deleted_at.is_(None))
        
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
    
    async def list_by_user(self, *, user_id: int, include_deleted: bool = False) -> list[UserRole]:
        stmt = select(UserRole).where(UserRole.user_id == user_id)
        
        if not include_deleted:
            stmt = stmt.where(UserRole.deleted_at.is_(None))
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def save(self, user_role: UserRole) -> UserRole:
        self.db.add(user_role)
        return user_role
    
    async def delete(self, user_role: UserRole) -> None:
        await self.db.delete(user_role)
