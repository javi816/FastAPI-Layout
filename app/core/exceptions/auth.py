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


class InvalidAuthorizationHeader(AuthenticationError):

    def __init__(self):
        super().__init__(
            message="Invalid authorization header",
            code="invalid_authorization_header",
            status_code=401
        )


class InvalidOrExpiredToken(AuthenticationError):

    def __init__(self):
        super().__init__(
            message="Invalid or expired token",
            code="invalid_or_expired_token",
            status_code=401
        )


class UserNotRegistered(AuthenticationError):

    def __init__(self):
        super().__init__(
            message="User not registered in system",
            code="user_not_registered",
            status_code=401
        )

