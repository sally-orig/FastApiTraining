from sqlalchemy import Table
from sqlalchemy.orm import relationship
from .db import Base, metadata, engine

vegetable_table = Table("PriceMonitor_vegetable", metadata, autoload_with=engine)
vegetable_action_table = Table("PriceMonitor_vegetableaction", metadata, autoload_with=engine)

class VegetableAction(Base):
    __table__ = vegetable_action_table
    vegetable = relationship("Vegetable", back_populates="actions")

    def __str__(self):
        return f'{self.id} - {self.tran_type}'

class Vegetable(Base):
    __table__ = vegetable_table
    actions = relationship("VegetableAction", back_populates="vegetable")

    def __str__(self):
        return f'{self.name} ({self.id})'


