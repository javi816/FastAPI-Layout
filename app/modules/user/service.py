

from .model import User, Role, UserRole
from .repository import UserRepository, RoleRepository, UserRoleRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    async def create_user(self, user: User) -> User:
        pass