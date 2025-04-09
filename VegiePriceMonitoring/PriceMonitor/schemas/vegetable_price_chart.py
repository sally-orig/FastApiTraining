from pydantic import BaseModel, Field
from typing import Any
from decimal import Decimal

class VegetablePriceChartBase(BaseModel):
    dates: list[str]
    prices: list[Decimal]

    class Config:
        from_attributes = True

class VegetablePriceChartView(VegetablePriceChartBase):
    highest_price: dict[Any, Any] = Field(description="Highest price and date")
    lowest_price: dict[Any, Any] = Field(description="Lowest price and date")
    max_price: Decimal