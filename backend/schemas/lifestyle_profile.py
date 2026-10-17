from pydantic import BaseModel

class LifestyleProfileCreate(BaseModel):
    sleep_hours:float |None=None
    water_intake:float| None=None
    exercise_days:int| None=None
    stress_level:int|None=None
    smoking:bool|None=None
    alcohol:bool|None=None
    sun_exposure_hours:float| None=None

class LifestyleProfileResponse(LifestyleProfileCreate):

    id:int
    user_id:int

    class Config:
        from_attributes=True