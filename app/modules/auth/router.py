from fastapi import APIRouter, Depends
from modules.user.model import User
from modules.auth.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "roles": [r.name for r in user.roles]
    }