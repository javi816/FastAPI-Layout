from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.db.uow import UnitOfWork
from app.db.deps import get_uow
from app.core.auth.provider import AuthProvider
from app.core.exceptions.auth import InvalidAuthorizationHeader
from app.modules.auth.schema import CurrentUser, FirebaseUser
from app.core.auth.deps import get_auth_provider
from app.modules.auth.service import AuthService


http_bearer = HTTPBearer(auto_error=False)


def get_auth_service(
    provider: AuthProvider = Depends(get_auth_provider),
    uow: UnitOfWork = Depends(get_uow)
) -> AuthService:
    return AuthService(provider=provider, uow=uow)


async def get_firebase_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    auth_service: AuthService = Depends(get_auth_service)
) -> FirebaseUser:
    if not credentials:
        raise InvalidAuthorizationHeader()

    return await auth_service.authenticate_firebase_user(credentials.credentials)


async def get_current_active_user(
    firebase_user: FirebaseUser = Depends(get_firebase_user),
    auth_service: AuthService = Depends(get_auth_service)
) -> CurrentUser:
    return await auth_service.get_current_active_user(firebase_user)