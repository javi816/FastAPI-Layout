import firebase_admin
from firebase_admin import credentials
from app.core.config import settings


def init_firebase() -> None:
    if not firebase_admin._apps:
        cred = credentials.Certificate({
            "type": "service_account",
            "proyect_id": settings.FIREBASE_PROJECT_ID,
            "private_key": settings.FIREBASE_PRIVATE_KEY,
            "client_email": settings.FIREBASE_CLIENT_EMAIL,
            "token_url": settings.FIREBASE_TOKEN_URL,
        })
        firebase_admin.initialize_app(cred)