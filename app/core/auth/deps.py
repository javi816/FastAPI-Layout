from app.core.auth.firebase_provider import FireBaseProvider
from app.core.auth.provider import AuthProvider

def get_auth_provider() -> AuthProvider:
    return FireBaseProvider