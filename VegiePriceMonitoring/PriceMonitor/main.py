from fastapi import FastAPI
from PriceMonitor.api.vegetable import router as vegetable_router
from PriceMonitor.api.vegetable_action import router as vegetable_action_router
from PriceMonitor.api.vegetable_price_chart import router as vegetable_price_chart_router

app = FastAPI()

app.include_router(vegetable_router, prefix="/vegetables", tags=["Vegetables"])
app.include_router(vegetable_action_router, prefix="/vegetable-actions", tags=["Vegetable Actions"])
app.include_router(vegetable_price_chart_router, prefix="/vegetable-price-chart", tags=["Vegetable Price Chart"])