from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime, UTC

from database import Base


class SkinScoreHistory(Base):
    __tablename__ = "skin_score_history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    total_score = Column(Integer, nullable=False)

    skin_condition_score = Column(Integer, nullable=False)
    lifestyle_score = Column(Integer, nullable=False)
    sleep_score = Column(Integer, nullable=False)
    routine_score = Column(Integer, nullable=False)
    hydration_score = Column(Integer, nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )