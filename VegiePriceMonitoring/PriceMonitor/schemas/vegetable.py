from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from .vegetable_action import VegetableActionBase

class VegetableBase(BaseModel):
    name: str
    description: str
    price: Decimal = Field(gt=0.01, decimal_places=2, max_digits=10)
    img: str

    class Config:
        from_attributes = True

class VegetableView(VegetableBase):
    updated_at: datetime

class VegetableCreate(VegetableBase):
    created_by: str
    created_at: datetime
    status: bool = True

class VegetableResponse(VegetableBase):
    id: int

    class Config:
        from_attributes = True
