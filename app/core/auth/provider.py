from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class AuthUser:
    def __init__(self, uid: str, email: str | None, name: str | None, provider: str | None):
        self.uid = uid
        self.email = email
        self.name = name
        self.provider = provider

class AuthProvider(ABC):
    @abstractmethod
    async def verify_token(self, token: str) -> AuthUser:
        pass