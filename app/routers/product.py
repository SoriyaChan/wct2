from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas import product as schemas
from app.crud import product as crud
from ..dependency import get_db, check_user_login
from typing import List

router = APIRouter(prefix="/product", tags=["product"])

@router.post("/create", response_model=schemas.Product)
def create_product(request: Request, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    username = check_user_login(db=db, request=request)
    return crud.create_product(db=db, product=product, created_by=username)

@router.get("/read", response_model=List[schemas.Product])
def read_products(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user = check_user_login(db=db, request=request)
    return crud.get_products(db=db, skip=skip, limit=limit)

@router.get("/read/{product_id}")
def read_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    user = check_user_login(db=db, request=request)
    return crud.get_product(db=db, product_id=product_id)

@router.put("/update")
def update_product(request: Request, product_id: int, product: schemas.ProductCreate ,db: Session = Depends(get_db)):
    username = check_user_login(db=db, request=request)
    return crud.update_product(db=db, product_id=product_id, updated_product=product, created_by=username)

@router.delete("/delete/{product_id}")
def delete_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    username = check_user_login(db=db, request=request)
    return crud.delete_product(db=db, product_id=product_id, username=username)

@router.get("/stock/read", response_model=List[schemas.Product_Inventory])
def read_product_stock(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user = check_user_login(db=db, request=request)
    return crud.get_product_stock(db=db, skip=skip, limit=limit)

@router.post("/category/create", response_model=schemas.ProductCategory)
def create_category(request: Request, category: schemas.ProductCategoryCreate, db: Session = Depends(get_db)):
    username = check_user_login(db=db, request=request)
    return crud.create_product_category(db=db, category=category, created_by=username)

@router.get("/category/read", response_model=List[schemas.ProductCategory])
def read_product_category(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user = check_user_login(db=db, request=request)
    return crud.get_product_category(db=db, skip=skip, limit=limit)