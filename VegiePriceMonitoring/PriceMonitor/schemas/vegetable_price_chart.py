from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal

class VegetablePriceChartBase(BaseModel):
    dates: list[str]
    prices: list[Decimal]
    highest_price: Decimal
    lowest_price: Decimal
    max_price: Decimal

    class Config:
        from_attributes = True

class VegetablePriceChartView(VegetablePriceChartBase):
    pass