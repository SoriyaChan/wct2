from sqlalchemy.orm import Session
from ..models import Product, Sale
from app.schemas import sale as schemas
from fastapi import HTTPException
from datetime import datetime, timedelta ,timezone

SEAsia = timezone(timedelta(hours=7))

def create_sale(db: Session, sale: schemas.SaleCreate, sold_by: str):
    product = db.query(Product).filter(Product.id == sale.product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < sale.quantity:
        raise HTTPException(status_code=409, detail="Not enough in stock")
    product.stock -= sale.quantity
    total_price = product.price*sale.quantity 
    transaction_date = datetime.now(SEAsia)
    db_sale = Sale(
        sold_by=sold_by,
        product_id=sale.product_id,
        quantity=sale.quantity,
        total_price=total_price,
        transaction_date=transaction_date,
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sale).offset(skip).limit(limit).all()