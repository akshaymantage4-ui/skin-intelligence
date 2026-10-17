from typing import Literal

from pydantic import BaseModel, EmailStr, Field

# Roles selectable at public registration. "administrator" is deliberately
# excluded here — that role must be granted by an existing administrator,
# never self-selected at signup.
PublicUserRole = Literal["user", "consultant", "dermatologist"]


class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str = Field(min_length=8)
    role: PublicUserRole = "user"


UserRole = Literal["user", "consultant", "dermatologist", "administrator"]


class UserRoleUpdate(BaseModel):
    role: UserRole


class AdminUserCreate(UserCreate):
    role: UserRole
