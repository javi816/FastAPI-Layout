from fastapi import Depends, Header, HTTPException, status
from app.db.uow import UnitOfWork
from app.db.deps import get_uow
from app.core.auth.provider import AuthProvider, AuthUser
from app.modules.auth.schema import CurrentUser
from app.core.auth.deps import get_auth_provider
from app.modules.user.model import User
from firebase_admin import auth

async def get_current_user(
    authorization: str = Header(...),
    provider: AuthProvider = Depends(get_auth_provider),
    uow: UnitOfWork = Depends(get_uow)
) -> CurrentUser:
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    token = authorization.replace("Bearer ", "").strip()
    
    try:
        auth_user = await provider.verify_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    async with uow:
        user = await uow.auth_identity_repository.get_user_by_provider_uid(
            provider=auth_user.provider,
            provider_uid=auth_user.uid
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not registered in system"
            )
        
    return CurrentUser(
        id=user.id,
        email=user.email,
        name=user.name,
        roles=[role.name for role in (user.roles or [])]
    )
