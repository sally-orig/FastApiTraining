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
    id: int
    updated_at: datetime
    status: bool

class VegetableCreate(VegetableBase):
    created_by: str

class VegetableResponse(BaseModel):
    id: int

class VegetableUpdate(BaseModel):
    price: Decimal = Field(gt=0.01, decimal_places=2, max_digits=10)
    description: str | None = None
    updated_by: str

class VegetableDeactivate(BaseModel):
    updated_by: str
