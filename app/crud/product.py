from sqlalchemy.orm import Session
from ..models import Product, Supplier
from app.schemas import product as schemas
from ..dependency import admin
from fastapi import HTTPException

def create_product(db: Session, product: schemas.ProductCreate, created_by: str):
    supplier_id = db.query(Supplier).filter(Supplier.id == product.supplier_id).first()
    if supplier_id is None:
        raise HTTPException(status_code=404, detail="Supplier not found") 
    if created_by != admin["name"]:
        raise HTTPException(status_code=403, detail="You do not have permission to create new records")
    db_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock,
        description=product.description,
        supplier_id=product.supplier_id,
        created_by=created_by)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def update_product(db: Session, product_id: int, updated_product: schemas.ProductCreate, created_by: str):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    supplier_id = db.query(Supplier).filter(Supplier.id == updated_product.supplier_id).first()
    if supplier_id is None:
        raise HTTPException(status_code=404, detail="Supplier not found") 
    if created_by != admin["name"]:
        raise HTTPException(status_code=403, detail="You do not have permission to update records")
    db_product.name = updated_product.name
    db_product.price = updated_product.price
    db_product.stock = updated_product.stock
    db_product.description = updated_product.description
    db_product.supplier_id = updated_product.supplier_id
    db_product.created_by = created_by
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int, username: str):
    if username != admin["name"]:
        raise HTTPException(status_code=403, detail="You do not have permission to delete records")
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product