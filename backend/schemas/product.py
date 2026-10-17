
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    brand: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=100)
    price: float = Field(ge=0)

    description: Optional[str] = None

    suitable_skin_types: List[str] = Field(default_factory=list)
    target_concerns: List[str] = Field(default_factory=list)
    ingredients: List[str] = Field(default_factory=list)
    avoids_allergies: List[str] = Field(default_factory=list)


class ProductResponse(ProductCreate):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)