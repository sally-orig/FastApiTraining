from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import status
from pathlib import Path
from ..core.db import get_db
from ..core.models import Vegetable, VegetableAction
from ..schemas.vegetable import VegetableCreate, VegetableView, VegetableResponse, VegetableUpdate
from ..use_cases.vegetable import VegetableUseCase


router = APIRouter()

def get_use_case(db: Session = Depends(get_db)) -> VegetableUseCase:
    return VegetableUseCase(db=db)

@router.get("/vegetables", response_model=list[VegetableView])
async def get_all_vegetables(use_case: VegetableUseCase = Depends(get_use_case)):
    vegetables = use_case.get_all_vegetables()
    if not vegetables:
        raise HTTPException(status_code=404, detail="No vegetable available")
    return vegetables

@router.get("/vegetables/{query}", response_model=list[VegetableView])
async def get_vegetable_by_name(query: str, use_case: VegetableUseCase = Depends(get_use_case)):
    vegetable = use_case.get_vegetable_by_name(query)
    if not vegetable:
        raise HTTPException(status_code=404, detail="Vegetable not found")
    return vegetable

@router.post("/vegetables", response_model=VegetableResponse, status_code=status.HTTP_201_CREATED)
async def create_vegetable(vegetable_data: VegetableCreate, use_case: VegetableUseCase = Depends(get_use_case)):  
    vegetable = use_case.create_vegetable(vegetable_data)
    return vegetable

@router.put("/vegetables/{vegetable_id}", response_model=VegetableResponse, status_code=status.HTTP_200_OK)
async def update_vegetable(vegetable_id: int, vegetable_data: VegetableUpdate, use_case: VegetableUseCase = Depends(get_use_case)):  
    vegetable = use_case.update_vegetable(vegetable_id, vegetable_data)
    return vegetable
    
    
