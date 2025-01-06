from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.schemas import product as schemas
from app.crud import product as crud
from ..dependency import get_db
from typing import List

router = APIRouter(prefix="/product", tags=["product"])

@router.post("/create", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, api_key: str = Header(...), db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product, api_key=api_key)

@router.get("/read", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db=db, skip=skip, limit=limit)

@router.get("/read/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db=db, product_id=product_id)

@router.put("/update")
def update_product(product_id: int, product: schemas.ProductCreate, api_key: str = Header(...), db: Session = Depends(get_db)):
    return crud.update_product(db=db, product_id=product_id, updated_product=product, api_key=api_key)

@router.delete("/delete/{product_id}")
def delete_product(product_id: int, api_key: str = Header(...), db: Session = Depends(get_db)):
    return crud.delete_product(db=db, product_id=product_id, api_key=api_key)

@router.get("/stock/read", response_model=List[schemas.Product_Inventory])
def read_product_stock(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_product_stock(db=db, skip=skip, limit=limit)

@router.post("/category/create", response_model=schemas.ProductCategory)
def create_category(category: schemas.ProductCategoryCreate, api_key: str = Header(...), db: Session = Depends(get_db)):
    return crud.create_product_category(db=db, category=category, api_key=api_key)

@router.get("/category/read", response_model=List[schemas.ProductCategory])
def read_product_category(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_product_category(db=db, skip=skip, limit=limit)