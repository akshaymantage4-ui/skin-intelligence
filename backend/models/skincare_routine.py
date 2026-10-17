from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class SkincareRoutine(Base):
    __tablename__ = "skincare_routines"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    morning_routine = Column(String(1000), nullable=True)

    evening_routine = Column(String(1000), nullable=True)

    weekly_routine = Column(String(1000), nullable=True)

    recommendations = Column(String(2000), nullable=True)