from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas import sale as schemas
from app.crud import sale as crud
from ..dependencies import get_db, check_user_login
from typing import List

router = APIRouter(prefix="/sale", tags=["sale"])

@router.post("/", response_model=schemas.Sale)
def create_sale(request: Request, sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    user = check_user_login(db=db, request=request)
    username = user.userName
    return crud.create_sale(db=db, sale=sale, sold_by=username)

@router.get("/", response_model=List[schemas.Sale])
def read_sales(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user = check_user_login(db=db, request=request)
    return crud.get_sales(db=db, skip=skip, limit=limit)