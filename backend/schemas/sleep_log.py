from pydantic import BaseModel
from datetime import date


class SleepLogCreate(BaseModel):

    sleep_date: date

    sleep_duration: float

    sleep_quality: str


class SleepLogResponse(BaseModel):

    id: int

    user_id: int

    sleep_date: date

    sleep_duration: float

    sleep_quality: str

    class Config:
        from_attributes = True