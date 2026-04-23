import pytest
from fastapi.testclient import TestClient
from app.main import app 

from app.core.auth.provider import AuthProvider, AuthUser
from app.modules.auth.deps import get_auth_provider

pytestmark = [pytest.mark.unit]

class TestAuthProvider(AuthProvider):
    def verify_token(self, token: str) -> AuthUser:
        return AuthUser(
            uid = "test-uid",
            email = "tes@email.com",
            name = "test-name"
        )

def override_auth_provider():
    return TestAuthProvider()

app.dependency_overrides[get_auth_provider] = override_auth_provider

client = TestClient(app)

def test_me_endpoint():
    response = client.get(
        "/me",
        headers = {"Authorization": "Bearer whatever"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["uid"] == "test-uid"
    assert data["email"] == "tes@email.com"
    assert data["ame"] == "test-name"