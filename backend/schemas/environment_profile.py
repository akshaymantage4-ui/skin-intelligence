from pydantic import BaseModel


class EnvironmentProfileCreate(BaseModel):
    location: str | None = None
    uv_index: float | None = None
    pollution_level: float | None = None
    temperature: float | None = None
    humidity: float | None = None
    water_quality: str | None = None


class EnvironmentProfileResponse(EnvironmentProfileCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True