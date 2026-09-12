from sqlalchemy import Column,Integer,Float,Boolean,ForeignKey
from database import Base

class LifestyleProfile(Base):
    __tablename__='lifestyle_profiles'

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey('users.id'),
                   nullable=False)

    sleep_hours=Column(Float,nullable=True)

    water_intake=Column(Float,nullable=True)
    exercise_days=Column(Integer,nullable=True)
    stress_level=Column(Integer,nullable=True)
    smoking=Column(Boolean,nullable=True)
    alcohol=Column(Boolean,nullable=True)
    sun_exposure_hours=Column(Float,nullable=True)