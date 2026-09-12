from sqlalchemy import Column,Integer,String,ForeignKey,Boolean
from database import Base

class SkinProfile(Base):
    __tablename__='skin_profiles'

    id=Column(Integer,primary_key=True,index=True)

    user_id=Column(Integer,
                   ForeignKey('users.id'),
                   nullable=False)


    skin_type=Column(String(50),nullable=False)
    acne=Column(Boolean,default=False)
    dryness=Column(Boolean,default=False)
    pigmentation=Column(Boolean,default=False)
    sensitivity=Column(Boolean,default=False)