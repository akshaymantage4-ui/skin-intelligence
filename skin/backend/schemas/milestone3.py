from datetime import date, datetime
from pydantic import BaseModel, Field

class IngredientAnalyzeRequest(BaseModel):
    ingredients: list[str] = Field(min_length=1, max_length=50)

class ProductRecommendationRequest(BaseModel):
    category: str | None = None
    budget: float | None = Field(default=None, ge=0)
    goal: str | None = None
    limit: int = Field(default=5, ge=1, le=20)

class ProgressLogCreate(BaseModel):
    log_date: date
    skin_score: float | None = Field(default=None, ge=0, le=100)
    routine_adherence: float | None = Field(default=None, ge=0, le=100)
    acne_level: str | None = None
    dryness_level: str | None = None
    pigmentation_level: str | None = None
    sensitivity_level: str | None = None
    notes: str | None = None

class ProgressLogResponse(ProgressLogCreate):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ProductCompareRequest(BaseModel):
    product_ids: list[int] = Field(min_length=2, max_length=4)
