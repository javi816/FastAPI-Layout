from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# User Schemas

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

    
class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

class UserAdminUpdate(UserUpdate):
    is_active: bool #pendiente


#Role Schemas


class RoleBase(BaseModel):
    name: str
    description: Optional[str]

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

class RoleRead(RoleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

