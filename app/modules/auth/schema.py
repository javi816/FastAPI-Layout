from pydantic import BaseModel
from typing import List, Optional

class CurrentUser(BaseModel):
    id: int
    email: Optional[str] = None
    name: Optional[str] = None

    roles: List[str]