from pydantic import BaseModel
from typing import List, Optional

class FirebaseUser(BaseModel):
    uid: str
    email: Optional[str] = None
    name: Optional[str] = None
    provider: str
    auth_identity_id: int
    user_id: int


class CurrentUser(BaseModel):
    id: int
    email: Optional[str] = None
    name: Optional[str] = None

    roles: List[str]