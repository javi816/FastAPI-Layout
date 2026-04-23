from fastapi import Depends, Header
from core.auth.provider import AuthProvider, AuthUser

def get_auth_provider() -> AuthProvider:
    
    raise NotImplementedError("Auth provider not configured")

def get_current_user(
    authorization: str = Header(...),
    provider: AuthProvider = Depends(get_auth_provider)
) -> AuthUser:
    token = authorization.replace("Bearer", "")
    return provider.verify_token(token)