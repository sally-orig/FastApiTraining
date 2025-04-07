from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from enum import Enum

class VegetableTransactionType(str, Enum):
    add_vegetable = "Add Vegetable"
    update_price = "Update Price"
    deactivate_vegetable = "Deactivate Vegetable"

class VegetableActionBase(BaseModel):
    created_at: datetime

    class Config:
        from_attributes = True

class VegetableView(VegetableActionBase):
    id: int
    tran_type: VegetableTransactionType
    vegetable_name: str
    details: str
    price: Decimal = Field(gt=0.01, decimal_places=2, max_digits=10)
    created_by: str

class VegetableActionResponse(VegetableActionBase):
    id: int

    class Config:
        from_attributes = True
