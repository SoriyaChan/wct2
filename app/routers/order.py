from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas import order as schemas
from app.crud import order as crud
from ..dependency import get_db, check_user_login
from typing import List

router = APIRouter(prefix="/order", tags=["order"])

@router.post("/", response_model=schemas.Order)
def create_order(request: Request, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    username = check_user_login(db=db, request=request)
    return crud.create_order(db=db, order=order, order_by=username)

@router.get("/", response_model=List[schemas.Order])
def read_orders(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user = check_user_login(db=db, request=request)
    return crud.get_orders(db=db, skip=skip, limit=limit)

@router.get("/orderproduct", response_model=List[schemas.OrderProductAssociation])
def read_orderproduct(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user = check_user_login(db=db, request=request)
    return crud.get_orderproduct(db=db, skip=skip, limit=limit)