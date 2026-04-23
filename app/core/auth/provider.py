from abc import ABC, abstractmethod

class AuthUser:
    def __init__(self, uid: str, email: str | None, name: str | None = None):
        self.uid = uid
        self.email = email
        self.name = name

class AuthProvider(ABC):
    @abstractmethod
    def verify_token(self, token: str) -> AuthUser:
        pass