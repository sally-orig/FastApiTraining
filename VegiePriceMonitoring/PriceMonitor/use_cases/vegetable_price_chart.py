from PriceMonitor.core.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from datetime import datetime
from ..core.models import VegetableAction
from ..schemas.vegetable_action import VegetableTransactionType
from ..schemas.vegetable_price_chart import VegetablePriceChartView

class VegetablePriceChartUseCase:
    def __init__(self, db: Session):
        self.db = db
        self.DEFAULT_VEGETABLE = "Kamatis"

    def get_vegetable_chart_data(self, selected_vegetable: str) -> VegetablePriceChartView:
        selected_vegetable = selected_vegetable if selected_vegetable else self.DEFAULT_VEGETABLE
        price_updates = (
            self.db.query(
                func.date(VegetableAction.created_at).label("date"),
                func.avg(VegetableAction.price).label("average_price")
            )
            .filter(
                (VegetableAction.tran_type ==  VegetableTransactionType.add_vegetable.name) |
                (VegetableAction.tran_type == VegetableTransactionType.update_price.name),
                VegetableAction.vegetable_name == selected_vegetable
            )
            .group_by(func.date(VegetableAction.created_at))
            .order_by(func.date(VegetableAction.created_at))
            .all()
        )

        if not price_updates:
            raise HTTPException(status_code=404, detail="No price updates available for the selected vegetable.")

        dates = []
        prices = []
        max_price = 0

        for update in price_updates:
            date_obj = datetime.strptime(update[0], "%Y-%m-%d")
            formatted_date = date_obj.strftime("%b-%d-%Y")
            dates.append(formatted_date)
            prices.append(float(update[1]))
            if update.average_price > max_price:
                max_price = update.average_price

        highest_price = max(prices, default=0)
        lowest_price = min(prices, default=0)

        return VegetablePriceChartView(
            vegetable_name=selected_vegetable,
            dates=dates,
            prices=prices,
            highest_price=highest_price,
            lowest_price=lowest_price,
            max_price=max_price
        )

