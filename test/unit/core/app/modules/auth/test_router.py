import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.modules.auth.schema import CurrentUser
from app.modules.auth.deps import get_current_active_user
from app.core.auth.provider import AuthProvider

pytestmark = [pytest.mark.unit]


class TestAuthRouter:
    @pytest.fixture
    def mock_current_user(self):
        return CurrentUser(
            id=1,
            email="test@example.com",
            name="Test User",
            roles=["admin"]
        )

    @pytest.fixture(autouse=True)
    def override_deps(self, mock_current_user):
        async def mock_get_current_active_user():
            return mock_current_user
        
        app.dependency_overrides[get_current_active_user] = mock_get_current_active_user
        yield
        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_me_endpoint_success(self, mock_current_user):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get(
                "/auth/me",
                headers={"Authorization": "Bearer valid_token"}
            )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
        assert data["roles"] == ["admin"]

    @pytest.mark.asyncio
    async def test_me_endpoint_no_authorization(self):
        app.dependency_overrides.clear()
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/auth/me")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_test_endpoint(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/auth/test")

        assert response.status_code == 200
        assert response.json() == "Si funca"