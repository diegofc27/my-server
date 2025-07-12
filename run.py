from fastapi import FastAPI

from src.api import product
from src.models.database import Base, engine

app = FastAPI()
app.include_router(product.router)

Base.metadata.create_all(bind=engine)
