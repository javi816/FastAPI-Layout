from app.core.exceptions.auth import (
    InvalidAuthorizationHeader,
    InvalidOrExpiredToken,
    UserNotActive,
)
from app.modules.auth.schema import CurrentUser, FirebaseUser
from app.modules.auth.model import AuthIdentity
from app.modules.user.model import User, Role, UserRole
from app.db.uow import UnitOfWork
from app.core.auth.provider import AuthProvider
from app.core.config import settings


class AuthService:
    def __init__(self, provider: AuthProvider, uow: UnitOfWork):
        self.provider = provider
        self.uow = uow

    def _get_bootstrap_admin_emails(self) -> set[str]:
        if not settings.BOOTSTRAP_ADMIN_EMAILS:
            return set()
        return {email.strip().lower() for email in settings.BOOTSTRAP_ADMIN_EMAILS.split(",") if email.strip()}

    async def authenticate_firebase_user(self, token: str) -> FirebaseUser:
        if not token:
            raise InvalidAuthorizationHeader()

        try:
            auth_user = await self.provider.verify_token(token)
        except Exception:
            raise InvalidOrExpiredToken()

        async with self.uow:
            identity = await self.uow.auth_identity_repository.get_identity_by_provider_uid(
                provider=auth_user.provider,
                provider_uid=auth_user.uid,
            )

            if not identity:
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
                await self.uow.session.flush()

        return FirebaseUser(
            uid=auth_user.uid,
            email=auth_user.email,
            name=auth_user.name,
            provider=auth_user.provider,
            auth_identity_id=identity.id,
            user_id=identity.user_id if identity.user_id else 0
        )

    async def get_current_active_user(self, firebase_user: FirebaseUser) -> CurrentUser:
        bootstrap_emails = self._get_bootstrap_admin_emails()

        async with self.uow:
            if firebase_user.user_id:
                user = await self.uow.user_repository.get_by_id(firebase_user.user_id, only_active=False, include_deleted=True)
            else:
                user = None

            if not user:
                user = User(
                    name=firebase_user.name or firebase_user.email.split("@")[0] if firebase_user.email else firebase_user.uid[:50],
                    email=firebase_user.email,
                    is_active=False,
                )
                await self.uow.user_repository.save(user)
                await self.uow.session.flush()

                identity = await self.uow.auth_identity_repository.get_by_id(firebase_user.auth_identity_id)
                if identity:
                    identity.user_id = user.id
                    await self.uow.session.flush()

            user_id = user.id
            user_email = user.email
            user_name = user.name

            is_bootstrap_admin = firebase_user.email and firebase_user.email.lower() in bootstrap_emails

            if is_bootstrap_admin and not user.is_active:
                user.is_active = True
                await self.uow.session.flush()

            if is_bootstrap_admin:
                superadmin_role = await self.uow.role_repository.get_by_name("superadmin")
                if not superadmin_role:
                    superadmin_role = Role(name="superadmin", description="Super Administrator")
                    await self.uow.role_repository.save(superadmin_role)
                    await self.uow.session.flush()

                existing_role = await self.uow.user_role_repository.get_by_user_and_role(user_id=user.id, role_id=superadmin_role.id)
                if not existing_role:
                    user_role = UserRole(user_id=user.id, role_id=superadmin_role.id)
                    await self.uow.user_role_repository.save(user_role)
                    await self.uow.session.flush()

            user_roles = [role.name for role in (user.roles or [])]

            if not user.is_active:
                raise UserNotActive()

        return CurrentUser(
            id=user_id,
            email=user_email,
            name=user_name,
            roles=user_roles,
        )