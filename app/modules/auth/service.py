from app.core.exceptions.auth import (
    InvalidAuthorizationHeader,
    InvalidOrExpiredToken,
)
from app.modules.auth.schema import CurrentUser
from app.modules.auth.model import AuthIdentity
from app.modules.user.model import User
from app.db.uow import UnitOfWork
from app.core.auth.provider import AuthProvider


class AuthService:
    def __init__(self, provider: AuthProvider, uow: UnitOfWork):
        self.provider = provider
        self.uow = uow

    async def get_current_user(self, authorization: str) -> CurrentUser:
        if not authorization.startswith("Bearer "):
            raise InvalidAuthorizationHeader()

        token = authorization.replace("Bearer ", "").strip()

        try:
            auth_user = await self.provider.verify_token(token)
        except Exception:
            raise InvalidOrExpiredToken()

        async with self.uow:
            user = await self.uow.auth_identity_repository.get_user_by_provider_uid(
                provider=auth_user.provider,
                provider_uid=auth_user.uid,
            )

            if not user:
                user = User(
                    name=auth_user.name or auth_user.email.split("@")[0] if auth_user.email else auth_user.uid[:50],
                    email=auth_user.email,
                    is_active=False,
                )
                await self.uow.user_repository.save(user)
                await self.uow.session.flush()

                identity = AuthIdentity(
                    user_id=user.id,
                    provider=auth_user.provider,
                    provider_uid=auth_user.uid,
                    provider_email=auth_user.email,
                )
                await self.uow.auth_identity_repository.save_identity(identity)
                
            user_id = user.id
            user_email = user.email
            user_name = user.name
            user_roles = [role.name for role in (user.roles or [])]

        return CurrentUser(
            id=user_id,
            email=user_email,
            name=user_name,
            roles=user_roles,
        )