from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import order as schemas
from app.crud import order as crud
from ..dependency import get_db
from typing import List

router = APIRouter(prefix="/order", tags=["order"])

@router.post("/create", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order)

@router.get("/read", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db=db, skip=skip, limit=limit)

@router.get("/read/orderproduct", response_model=List[schemas.OrderProductAssociation])
def read_orderproduct(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orderproduct(db=db, skip=skip, limit=limit)