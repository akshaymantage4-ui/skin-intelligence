from pydantic import BaseModel


class SkinAssessmentCreate(BaseModel):

    skin_type: str

    acne_level: str | None = None

    dryness_level: str | None = None

    pigmentation_level: str | None = None

    sensitivity_level: str | None = None

    additional_concerns: str | None = None


class SkinAssessmentResponse(SkinAssessmentCreate):

    id: int

    user_id: int

    class Config:
        from_attributes = True