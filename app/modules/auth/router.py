from fastapi import APIRouter, Depends
from app.modules.user.model import User
from app.modules.auth.deps import get_current_user, firebase_only_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "roles": [r.name for r in user.roles]
    }
    
@router.get("/firebase-test")
def firebase_test(user = Depends(firebase_only_current_user)):
    return user