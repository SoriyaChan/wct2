from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas import supplier as schemas
from app.crud import supplier as crud
from ..dependency import get_db, check_user_login
from typing import List

router = APIRouter(prefix="/supplier", tags=["supplier"])

@router.post("/create", response_model=schemas.Supplier)
def create_supplier(request: Request, supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    username = check_user_login(db=db, request=request)
    return crud.create_supplier(db=db, supplier=supplier, created_by=username)

@router.get("/read", response_model=List[schemas.Supplier])
def read_suppliers(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user = check_user_login(db=db, request=request)
    return crud.get_suppliers(db=db, skip=skip, limit=limit)

@router.get("/read/{supplier_phone}")
def read_supplier(request: Request, supplier_phone: str, db: Session = Depends(get_db)):
    user = check_user_login(db=db, request=request)
    return crud.get_supplier(db=db, phone=supplier_phone)

