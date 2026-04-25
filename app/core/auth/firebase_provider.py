from firebase_admin import auth
from fastapi.concurrency import run_in_threadpool

from app.core.auth.provider import AuthProvider, AuthUser


class FireBaseProvider(AuthProvider):
    async def verify_token(self, token) -> AuthUser:
        decoded = await run_in_threadpool(auth.verify_id_token, token)
        
        return AuthUser(
            uid=decoded["uid"],
            email=decoded.get("email"),
            provider=decoded.get("firebase", {}).get("sign_in_provider")
        )