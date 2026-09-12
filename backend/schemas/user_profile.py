from pydantic import BaseModel

class UserProfileCreate(BaseModel):
    age:int | None=None
    gender:str | None=None
    location:str | None=None

class UserProfileResponse(BaseModel):
    id:int
    user_id:int
    age:int|None=None
    gender:str|None=None
    location:str|None=None

    class Config:
        from_attributes=True