from sqlalchemy import Column,Integer,String,ForeignKey
from database import Base

class UserProfile(Base):
    __tablename__="user_profiles"
    id =Column(Integer,primary_key=True,index=True)

    user_id=Column(
        Integer,
        # foreign key mule unique profile create hotat
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    age=Column(Integer,nullable=True)
    gender=Column(String(20),nullable=True)
    location=Column(String(100),nullable=True)