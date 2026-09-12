from sqlalchemy import Column, Integer, Float, String, ForeignKey
from database import Base


class EnvironmentProfile(Base):
    __tablename__ = "environment_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    location = Column(String, nullable=True)
    uv_index = Column(Float, nullable=True)
    pollution_level = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    water_quality = Column(String, nullable=True)