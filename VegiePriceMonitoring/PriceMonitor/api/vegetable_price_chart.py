from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import status
from fastapi import Query
from ..core.db import get_db
from ..schemas.vegetable_price_chart import VegetablePriceChartView
from ..use_cases.vegetable_price_chart import VegetablePriceChartUseCase


router = APIRouter()

def get_use_case(db: Session = Depends(get_db)) -> VegetablePriceChartUseCase:
    return VegetablePriceChartUseCase(db=db)

@router.get("", response_model=VegetablePriceChartView, status_code=status.HTTP_200_OK)
async def get_all_vegetable_actions(selected_vegetable: str = Query(default="Kamatis", description="Values can be obtained from get_all_vegetables api"), use_case: VegetablePriceChartUseCase = Depends(get_use_case)):
    chart_data = use_case.get_vegetable_chart_data(selected_vegetable)
    if not chart_data:
        raise HTTPException(status_code=404, detail="No chart data available")
    return chart_data