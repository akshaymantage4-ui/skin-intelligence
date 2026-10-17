from datetime import datetime, UTC
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from database import Base

class ProductRecommendationHistory(Base):
    __tablename__ = "product_recommendation_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    request_json = Column(Text, nullable=False)
    result_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
