from pydantic import BaseModel

class SkinProfileCreate(BaseModel):
    skin_type:str
    acne:bool=False
    dryness:bool=False
    pigmentation:bool=False
    sensitivity:bool=False


class SkinProfileResponse(BaseModel):
    id:int
    user_id:int
    skin_type:str
    acne:bool
    dryness:bool
    pigmentation:bool
    sensitivity:bool


    class Config:
        from_attributes=True