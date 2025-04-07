from fastapi import FastAPI
from PriceMonitor.api.vegetable import router as vegetable_router

app = FastAPI()

app.include_router(vegetable_router, prefix="/vegetable", tags=["vegetable"])