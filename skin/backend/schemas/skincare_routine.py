from pydantic import BaseModel


class SkincareRoutineCreate(BaseModel):

    morning_routine: str | None = None

    evening_routine: str | None = None

    weekly_routine: str | None = None

    recommendations: str | None = None


class SkincareRoutineResponse(SkincareRoutineCreate):

    id: int

    user_id: int

    class Config:
        from_attributes = True