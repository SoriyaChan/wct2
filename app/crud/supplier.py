from sqlalchemy.orm import Session
from ..models import Supplier
from app.schemas import supplier as schemas
from ..dependency import admin
from fastapi import HTTPException

def create_supplier(db: Session, supplier: schemas.SupplierCreate, created_by: str):
    # if not admin, can't create
    if created_by != admin["name"]:
        raise HTTPException(status_code=403, detail="You do not have permission to create new records") 
    # query existing phone
    checksupplier = db.query(Supplier).filter(Supplier.phone == supplier.phone).first()
    # if there is, can't create
    if checksupplier:
        raise HTTPException(status_code=403, detail="Supplier can't be create") 
    # add supplier
    db_supplier = Supplier(supplier_name=supplier.supplier_name, address=supplier.address, phone=supplier.phone, created_by=created_by)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def get_suppliers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Supplier).offset(skip).limit(limit).all()

def get_supplier(db: Session, phone: str):
    # query existing phone 
    supplier = db.query(Supplier).filter(Supplier.phone == phone).first()
    # if none
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier
