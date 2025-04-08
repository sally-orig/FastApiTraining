from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..core.models import VegetableAction
from ..schemas.vegetable_action import VegetableActionView

class VegetableActionUseCase:
    def __init__(self, db: Session):
        self.db = db

    def generate_vegetable_action_view(self, vegetable_action: VegetableAction) -> VegetableActionView:
        return VegetableActionView(**vegetable_action.__dict__)

    def get_all_vegetable_actions(self) -> list[VegetableActionView]:
        result = self.db.query(VegetableAction).order_by(desc(VegetableAction.id)).all()
        result = [self.generate_vegetable_action_view(veg_action) for veg_action in result]
        return result