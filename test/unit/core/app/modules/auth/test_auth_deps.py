import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.security import HTTPAuthorizationCredentials
from app.modules.auth.deps import get_firebase_user, get_current_active_user, http_bearer, get_auth_service
from app.modules.auth.service import AuthService
from app.modules.auth.schema import FirebaseUser, CurrentUser
from app.modules.user.model import User
from app.core.auth.provider import AuthProvider, AuthUser
from app.db.uow import UnitOfWork
from app.core.exceptions.auth import InvalidAuthorizationHeader, InvalidOrExpiredToken, UserNotActive

pytestmark = [pytest.mark.unit]


class TestAuthServiceMethods:
    @pytest.fixture
    def mock_provider(self):
        provider = MagicMock(spec=AuthProvider)
        provider.verify_token = AsyncMock()
        return provider

    @pytest.fixture
    def mock_uow(self):
        uow = MagicMock(spec=UnitOfWork)
        uow.__aenter__ = AsyncMock(return_value=uow)
        uow.__aexit__ = AsyncMock(return_value=None)
        uow.auth_identity_repository = MagicMock()
        uow.user_repository = MagicMock()
        uow.role_repository = MagicMock()
        uow.user_role_repository = MagicMock()
        uow.session = MagicMock()
        uow.session.flush = AsyncMock()
        return uow

    @pytest.fixture
    def auth_service(self, mock_provider, mock_uow):
        return AuthService(provider=mock_provider, uow=mock_uow)

    @pytest.mark.asyncio
    async def test_authenticate_firebase_user_success_existing_identity(self, auth_service, mock_provider, mock_uow):
        auth_user = AuthUser(
            uid="firebase-123",
            email="user@example.com",
            name="Test User",
            provider="firebase"
        )
        mock_provider.verify_token.return_value = auth_user

        mock_identity = MagicMock()
        mock_identity.id = 1
        mock_identity.user_id = 10
        mock_uow.auth_identity_repository.get_identity_by_provider_uid = AsyncMock(return_value=mock_identity)

        result = await auth_service.authenticate_firebase_user("valid_token")

        assert isinstance(result, FirebaseUser)
        assert result.uid == "firebase-123"
        assert result.email == "user@example.com"
        assert result.auth_identity_id == 1
        assert result.user_id == 10

    @pytest.mark.asyncio
    async def test_authenticate_firebase_user_creates_new_identity_if_not_exists(self, auth_service, mock_provider, mock_uow):
        auth_user = AuthUser(
            uid="firebase-new",
            email="new@example.com",
            name="New User",
            provider="firebase"
        )
        mock_provider.verify_token.return_value = auth_user

        mock_uow.auth_identity_repository.get_identity_by_provider_uid = AsyncMock(return_value=None)

        saved_identity = MagicMock()
        saved_identity.id = 1
        saved_identity.user_id = None

        async def mock_save(identity):
            identity.id = 1

        mock_uow.auth_identity_repository.save_identity = AsyncMock(side_effect=mock_save)
        mock_uow.session.flush = AsyncMock()

        result = await auth_service.authenticate_firebase_user("new_token")

        mock_uow.auth_identity_repository.save_identity.assert_called_once()
        assert result.uid == "firebase-new"
        assert result.user_id == 0

    @pytest.mark.asyncio
    async def test_authenticate_firebase_user_invalid_token_raises_exception(self, auth_service, mock_provider, mock_uow):
        mock_provider.verify_token.side_effect = Exception("Invalid token")

        with pytest.raises(InvalidOrExpiredToken):
            await auth_service.authenticate_firebase_user("invalid_token")

    @pytest.mark.asyncio
    async def test_get_current_active_user_existing_active_user(self, auth_service, mock_uow):
        firebase_user = FirebaseUser(
            uid="firebase-123",
            email="user@example.com",
            name="Test User",
            provider="firebase",
            auth_identity_id=1,
            user_id=10
        )

        mock_role = MagicMock()
        mock_role.name = "admin"

        mock_user = MagicMock(spec=User)
        mock_user.id = 10
        mock_user.email = "user@example.com"
        mock_user.name = "Test User"
        mock_user.is_active = True
        mock_user.roles = [mock_role]

        mock_uow.user_repository.get_by_id = AsyncMock(return_value=mock_user)

        result = await auth_service.get_current_active_user(firebase_user)

        assert isinstance(result, CurrentUser)
        assert result.id == 10
        assert result.email == "user@example.com"
        assert result.roles == ["admin"]

    @pytest.mark.asyncio
    async def test_get_current_active_user_inactive_user_raises_exception(self, auth_service, mock_uow):
        firebase_user = FirebaseUser(
            uid="firebase-123",
            email="user@example.com",
            name="Test User",
            provider="firebase",
            auth_identity_id=1,
            user_id=10
        )

        mock_user = MagicMock(spec=User)
        mock_user.id = 10
        mock_user.email = "user@example.com"
        mock_user.name = "Test User"
        mock_user.is_active = False
        mock_user.roles = []

        mock_uow.user_repository.get_by_id = AsyncMock(return_value=mock_user)

        with pytest.raises(UserNotActive):
            await auth_service.get_current_active_user(firebase_user)

    @pytest.mark.asyncio
    async def test_get_current_active_user_returns_user_with_roles(self, auth_service, mock_uow):
        mock_role = MagicMock()
        mock_role.name = "user"

        mock_user = MagicMock(spec=User)
        mock_user.id = 10
        mock_user.email = "test@example.com"
        mock_user.name = "Test User"
        mock_user.is_active = True
        mock_user.roles = [mock_role]

        mock_uow.user_repository.get_by_id = AsyncMock(return_value=mock_user)

        firebase_user = FirebaseUser(
            uid="firebase-123",
            email="test@example.com",
            name="Test User",
            provider="firebase",
            auth_identity_id=1,
            user_id=10
        )

        result = await auth_service.get_current_active_user(firebase_user)

        assert result.id == 10
        assert result.email == "test@example.com"
        assert result.roles == ["user"]

    def test_get_bootstrap_admin_emails_parses_env_variable(self, auth_service):
        with patch("app.modules.auth.service.settings") as mock_settings:
            mock_settings.BOOTSTRAP_ADMIN_EMAILS = "admin1@gmail.com,admin2@gmail.com"
            result = auth_service._get_bootstrap_admin_emails()
            assert "admin1@gmail.com" in result
            assert "admin2@gmail.com" in result

    def test_get_bootstrap_admin_emails_empty_returns_empty_set(self, auth_service):
        with patch("app.modules.auth.service.settings") as mock_settings:
            mock_settings.BOOTSTRAP_ADMIN_EMAILS = ""
            result = auth_service._get_bootstrap_admin_emails()
            assert result == set()


class TestGetAuthService:
    @pytest.fixture
    def mock_provider(self):
        return MagicMock(spec=AuthProvider)

    @pytest.fixture
    def mock_uow(self):
        return MagicMock(spec=UnitOfWork)

    def test_get_auth_service_returns_auth_service_instance(self, mock_provider, mock_uow):
        service = get_auth_service(provider=mock_provider, uow=mock_uow)

        assert isinstance(service, AuthService)
        assert service.provider == mock_provider
        assert service.uow == mock_uow


class TestGetFirebaseUser:
    @pytest.fixture
    def mock_auth_service(self):
        service = MagicMock(spec=AuthService)
        service.authenticate_firebase_user = AsyncMock()
        return service

    @pytest.mark.asyncio
    async def test_get_firebase_user_calls_service(self, mock_auth_service):
        expected_firebase_user = FirebaseUser(
            uid="firebase-123",
            email="test@example.com",
            name="Test",
            provider="firebase",
            auth_identity_id=1,
            user_id=10
        )
        mock_auth_service.authenticate_firebase_user.return_value = expected_firebase_user

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="valid_token"
        )

        result = await get_firebase_user(
            credentials=credentials,
            auth_service=mock_auth_service
        )

        mock_auth_service.authenticate_firebase_user.assert_called_once_with("valid_token")
        assert result == expected_firebase_user

    @pytest.mark.asyncio
    async def test_get_firebase_user_no_credentials_raises_exception(self, mock_auth_service):
        with pytest.raises(InvalidAuthorizationHeader):
            await get_firebase_user(
                credentials=None,
                auth_service=mock_auth_service
            )


class TestGetCurrentActiveUser:
    @pytest.fixture
    def mock_auth_service(self):
        service = MagicMock(spec=AuthService)
        service.get_current_active_user = AsyncMock()
        return service

    @pytest.mark.asyncio
    async def test_get_current_active_user_calls_service(self, mock_auth_service):
        expected_user = CurrentUser(
            id=1,
            email="test@example.com",
            name="Test User",
            roles=["admin"]
        )
        mock_auth_service.get_current_active_user.return_value = expected_user

        firebase_user = FirebaseUser(
            uid="firebase-123",
            email="test@example.com",
            name="Test User",
            provider="firebase",
            auth_identity_id=1,
            user_id=10
        )

        result = await get_current_active_user(
            firebase_user=firebase_user,
            auth_service=mock_auth_service
        )

        mock_auth_service.get_current_active_user.assert_called_once_with(firebase_user)
        assert result == expected_user


class TestHTTPBearer:
    def test_http_bearer_auto_error_false(self):
        assert http_bearer.auto_error is False

    def test_http_bearer_is_bearer_type(self):
        assert "Bearer" in str(type(http_bearer).__name__)