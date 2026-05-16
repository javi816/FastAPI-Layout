from fastapi import APIRouter, Depends
from app.modules.auth.deps import get_current_active_user
from app.modules.auth.schema import CurrentUser

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/me")
async def me(user: CurrentUser = Depends(get_current_active_user)):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "roles": user.roles
    }

@router.get("/test")
async def test():
    return f"Si funca"