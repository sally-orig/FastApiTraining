from sqlalchemy.orm import Session
from datetime import datetime
from ..core.models import Vegetable, VegetableAction
from ..schemas.vegetable import VegetableCreate, VegetableView, VegetableResponse
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
        vegetable_action = VegetableAction(
            tran_type=VegetableTransactionType.add_vegetable,
            vegetable_name=vegetable_data.name,
            created_at=datetime.now(),
            details="Vegetable created",
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
            created_at=vegetable_data.created_at,
            status=vegetable_data.status,
            tran_id_id = vegetable_action.id,
        )
        self.db.add(vegetable)
        self.db.commit()
        self.db.refresh(vegetable)

        return VegetableResponse(
            id=vegetable.id,
            name=vegetable.name,
            description=vegetable.description,
            price=vegetable.price,
            img=vegetable.img)
