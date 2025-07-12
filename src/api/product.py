from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import src.services.product_service as service
from src.models.database import SessionLocal

router = APIRouter()


class ProductSchema(BaseModel):
    name: str
    description: str
    price: float


class ProductOut(ProductSchema):
    id: int

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/products", response_model=List[ProductOut])
def read_products(db: Session = Depends(get_db)):
    return service.get_products(db)


@router.get("/products/{product_id}", response_model=ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products", response_model=ProductOut)
def create(product: ProductSchema, db: Session = Depends(get_db)):
    return service.create_product(db, product)


@router.put("/products/{product_id}", response_model=ProductOut)
def update(product_id: int, product: ProductSchema, db: Session = Depends(get_db)):
    updated = service.update_product(db, product_id, product)
    if updated is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.delete("/products/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):
    deleted = service.delete_product(db, product_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}
