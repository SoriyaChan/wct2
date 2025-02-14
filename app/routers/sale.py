from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import sale as schemas
from app.crud import sale as crud
from ..dependency import get_db
from typing import List

router = APIRouter(prefix="/sale", tags=["sale"])

@router.post("/create", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    return crud.create_sale(db=db, sale=sale)

@router.get("/read", response_model=List[schemas.Sale])
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_sales(db=db, skip=skip, limit=limit)

@router.get("/read/saleproduct", response_model=List[schemas.SaleProductAssociation])
def read_saleproduct(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_saleproduct(db=db, skip=skip, limit=limit)