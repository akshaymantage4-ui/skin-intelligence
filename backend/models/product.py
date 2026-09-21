from sqlalchemy import(
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    JSON,

)
from database import Base
class Product(Base):
    __tablename__="products"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(150),nullable=False)
    brand=Column(String(100),nullable=False)
    category=Column(String(100),nullable=False)
    price=Column(Float,nullable=False)
    description=Column(Text,nullable=True)
    suitable_skin_types=Column(JSON,nullable=False)
    target_concerns=Column(JSON,nullable=False)
    ingredients=Column(JSON,nullable=False)
    avoids_allergies=Column(JSON,nullable=False,default=list)
    is_active=Column(Boolean,default=True)