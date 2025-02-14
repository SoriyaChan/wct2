from sqlalchemy.orm import Session
from ..models import Supplier, User
from app.schemas import supplier as schemas
from fastapi import HTTPException, Header

def create_supplier(db: Session, supplier: schemas.SupplierCreate, api_key: str = Header(...)):
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create supplier")
    # query existing phone
    checksupplier = db.query(Supplier).filter(Supplier.phone == supplier.phone).first()
    # if there is, can't create
    if checksupplier:
        raise HTTPException(status_code=403, detail="Supplier with this phone number already exists") 
    # add supplier
    db_supplier = Supplier(supplier_name=supplier.supplier_name, address=supplier.address, phone=supplier.phone)
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