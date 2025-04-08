from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import status
from ..core.db import get_db
from ..schemas.vegetable_action import VegetableActionView
from ..use_cases.vegetable_action import VegetableActionUseCase


router = APIRouter()

def get_use_case(db: Session = Depends(get_db)) -> VegetableActionUseCase:
    return VegetableActionUseCase(db=db)

@router.get("", response_model=list[VegetableActionView], status_code=status.HTTP_200_OK)
async def get_all_vegetable_actions(use_case: VegetableActionUseCase = Depends(get_use_case)):
    vegetable_actions = use_case.get_all_vegetable_actions()
    if not vegetable_actions:
        raise HTTPException(status_code=404, detail="No vegetable actions available")
    return vegetable_actions