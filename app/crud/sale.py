from sqlalchemy.orm import Session
from sqlalchemy import insert
from ..models import Product, Sale, SaleProductAssociation
from app.schemas import sale as schemas
from fastapi import HTTPException
from datetime import datetime, timedelta ,timezone

SEAsia = timezone(timedelta(hours=7))

def create_sale(db: Session, sale: schemas.SaleCreate, sold_by: str):
    total_price = 0

    for sale_product in sale.products:
        product = db.query(Product).filter(Product.id == sale_product.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {sale_product.product_id} not found.")
        if product.stock < sale_product.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product ID {sale_product.product_id}. Available: {product.stock}, Requested: {sale_product.quantity}"
            )
        
        total_price += sale_product.quantity * product.price
        product.stock -= sale_product.quantity

    db_sale = Sale(
        sold_by=sold_by,
        total_price=total_price,
        transaction_date=datetime.now(SEAsia)
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    
    for sale_product in sale.products:
        stmt = insert(SaleProductAssociation).values(
            sale_id=db_sale.id,
            product_id=sale_product.product_id,
            quantity=sale_product.quantity,
            price_at_sale=product.price
        )
        db.execute(stmt)
    
    db.commit()
    return db_sale


def get_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sale).offset(skip).limit(limit).all()