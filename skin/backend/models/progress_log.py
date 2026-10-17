from datetime import datetime, UTC
from sqlalchemy import Column, Integer, Float, String, Text, Date, DateTime, ForeignKey
from database import Base

class ProgressLog(Base):
    __tablename__ = "progress_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    log_date = Column(Date, nullable=False)
    skin_score = Column(Float, nullable=True)
    routine_adherence = Column(Float, nullable=True)
    acne_level = Column(String(20), nullable=True)
    dryness_level = Column(String(20), nullable=True)
    pigmentation_level = Column(String(20), nullable=True)
    sensitivity_level = Column(String(20), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
