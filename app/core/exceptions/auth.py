from .base import DomainException


class AuthenticationError(DomainException):
    """Base exception for authenticatio/authorization errors"""
    pass

class InvalidCredentials(AuthenticationError):
    
    def __init__(self):
        super().__init__(
            message="Credenciales invalidas",
            code="invalid_credentials",
            status_code=401
        )

class UserNotActive(AuthenticationError):
    
    def __init__(self):
        super().__init__(
            message="El usuario no está activo",
            code="user_not_active",
            status_code=403
        )

class UserNotFound(AuthenticationError):
    
    def __init__(self):
        super().__init__(
            message="Usuario no encontrado",
            code="user_not_found",
            status_code=404
        )

