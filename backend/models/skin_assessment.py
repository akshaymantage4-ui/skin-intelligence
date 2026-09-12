from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class SkinAssessment(Base):
    __tablename__ = "skin_assessments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    skin_type = Column(String(50), nullable=False)

    acne_level = Column(String(20), nullable=True)
    dryness_level = Column(String(20), nullable=True)
    pigmentation_level = Column(String(20), nullable=True)
    sensitivity_level = Column(String(20), nullable=True)

    additional_concerns = Column(String(500), nullable=True)