from typing import Literal

from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str = Field(min_length=8)


UserRole = Literal["user", "consultant", "dermatologist", "administrator"]


class UserRoleUpdate(BaseModel):
    role: UserRole


class AdminUserCreate(UserCreate):
    role: UserRole
