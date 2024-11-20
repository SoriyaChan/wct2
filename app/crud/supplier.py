from sqlalchemy.orm import Session
from ..models import Supplier
from app.schemas import supplier as schemas
from fastapi import HTTPException

def create_supplier(db: Session, supplier: schemas.SupplierCreate):
    supplier_id = db.query(Supplier).filter(Supplier.phone == supplier.phone).first()
    if supplier_id:
        raise HTTPException(status_code=403, detail="Supplier can't be create") 
    db_supplier = Supplier(name=supplier.name, address=supplier.address, phone=supplier.phone)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def get_suppliers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Supplier).offset(skip).limit(limit).all()

def get_supplier(db: Session, phone: str):
    supplier = db.query(Supplier).filter(Supplier.phone == phone).first()
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier
