from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from ..core.models import Vegetable, VegetableAction
from ..schemas.vegetable import VegetableCreate, VegetableView, VegetableResponse, VegetableUpdate, VegetableDeactivate
from ..schemas.vegetable_action import VegetableTransactionType

class VegetableUseCase:
    def __init__(self, db: Session):
        self.db = db

    def generate_vegetable_view(self, vegetable: Vegetable) -> VegetableView:
        return VegetableView(
            name=vegetable.name,
            description=vegetable.description,
            price=vegetable.price,
            updated_at=vegetable.actions.created_at,
            img=vegetable.img,
            status=vegetable.status,
            id=vegetable.id,
        )

    def get_all_vegetables(self) -> list[VegetableView]:
        result = self.db.query(Vegetable).filter(Vegetable.status == True).order_by(Vegetable.name).all()
        result = [self.generate_vegetable_view(veg) for veg in result]
        return result

    def get_vegetable_by_name(self, query: str) -> list[VegetableView]:
        result = self.db.query(Vegetable).filter(Vegetable.name.ilike(f"%{query}%"), Vegetable.status == True).order_by(Vegetable.name).all()
        result = [self.generate_vegetable_view(veg) for veg in result]
        return result

    def create_vegetable(self, vegetable_data: VegetableCreate) -> VegetableResponse:
        try:    
            vegetable_action = VegetableAction(
                tran_type=VegetableTransactionType.add_vegetable,
                vegetable_name=vegetable_data.name,
                created_at=datetime.now(),
                details=f"Vegetable created: {vegetable_data.name}",
                price=vegetable_data.price,
                created_by=vegetable_data.created_by,
            )
            self.db.add(vegetable_action)
            self.db.commit()
            self.db.refresh(vegetable_action)

            vegetable = Vegetable(
                name=vegetable_data.name,
                description=vegetable_data.description,
                price=vegetable_data.price,
                img=vegetable_data.img,
                created_by=vegetable_data.created_by,
                created_at=datetime.now(),
                status=True,
                tran_id_id = vegetable_action.id,
            )
            self.db.add(vegetable)
            self.db.commit()
            self.db.refresh(vegetable)
            return VegetableResponse(id=vegetable.id)
        
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating vegetable: {str(e)}")
        
    def get_vegetable_by_id(self, vegetable_id: int) -> Vegetable:
        vegetable = self.db.query(Vegetable).filter(Vegetable.id == vegetable_id).first()
        if not vegetable:
            raise HTTPException(status_code=404, detail="Vegetable not found")
        return vegetable
    
    def update_vegetable(self, vegetable_id: int, vegetable_data: VegetableUpdate) -> VegetableResponse:   
        vegetable = self.get_vegetable_by_id(vegetable_id)
        try:
            vegetable_action = VegetableAction(
                tran_type=VegetableTransactionType.update_price,
                vegetable_name=vegetable.name,
                created_at=datetime.now(),
                details=f"Vegetable price updated: {vegetable.name}",
                price=vegetable_data.price,
                created_by=vegetable_data.updated_by,
            )
            self.db.add(vegetable_action)
            self.db.commit()
            self.db.refresh(vegetable_action)

            vegetable.price = vegetable_data.price
            vegetable.description = vegetable_data.description if vegetable_data.description else vegetable.description
            vegetable.tran_id_id = vegetable_action.id
            self.db.commit()
            self.db.refresh(vegetable)

            return VegetableResponse(id=vegetable.id)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating vegetable: {str(e)}")
        
    def deactivate_vegetable(self, vegetable_id: int, vegetable_data: VegetableDeactivate) -> VegetableResponse:
        vegetable = self.get_vegetable_by_id(vegetable_id)
        try:
            vegetable_action = VegetableAction(
                tran_type=VegetableTransactionType.deactivate_vegetable,
                vegetable_name=vegetable.name,
                created_at=datetime.now(),
                details=f"Vegetable deactivated: {vegetable.name}",
                price=vegetable.price,
                created_by=vegetable_data.updated_by,
            )
            self.db.add(vegetable_action)
            self.db.commit()
            self.db.refresh(vegetable_action)

            vegetable.status = False
            vegetable.tran_id_id = vegetable_action.id
            self.db.commit()
            self.db.refresh(vegetable)

            return VegetableResponse(id=vegetable.id)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error deactivating vegetable: {str(e)}")
