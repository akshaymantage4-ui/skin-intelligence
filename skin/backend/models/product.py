from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    JSON,
    Boolean
)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(120), nullable=False)
    category = Column(String(60), nullable=False, index=True)
    price = Column(Float, nullable=False)

    skin_types = Column("suitable_skin_types", JSON, nullable=False)
    concerns = Column("target_concerns", JSON, nullable=False)
    key_ingredients = Column("ingredients", JSON, nullable=False)

    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)