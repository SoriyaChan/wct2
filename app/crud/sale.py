from sqlalchemy.orm import Session
from sqlalchemy import insert
from ..models import Product, Sale, SaleProductAssociation, Product_Inventory
from app.schemas import sale as schemas
from fastapi import HTTPException
from datetime import datetime, timedelta ,timezone

SEAsia = timezone(timedelta(hours=7))

def create_sale(db: Session, sale: schemas.SaleCreate, sold_by: str):
    total_price = 0
    # loop product in products
    for sale_product in sale.products:
        # check and get product
        product = db.query(Product).filter(Product.product_id == sale_product.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {sale_product.product_id} not found.")
        # check and get product stock
        product_stock = db.query(Product_Inventory).filter(Product_Inventory.product_id == sale_product.product_id).first()
        if not product_stock:
            raise HTTPException(status_code=404, detail=f"Product ID {sale_product.product_id} has no stock.")
        # if stock not enough
        if product_stock.stock < sale_product.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product ID {sale_product.product_id}. Available: {product_stock.stock}, Requested: {sale_product.quantity}"
            )
        # sell price = 1.1 orginal price, increment total price, minus stock
        sale_price = product.unit_price * 1.1
        total_price += sale_product.quantity * sale_price
        product_stock.stock -= sale_product.quantity
    # add sale
    db_sale = Sale(
        sold_by=sold_by,
        total_price=total_price,
        sale_date=datetime.now(SEAsia)
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    # loop product in products
    for sale_product in sale.products:
        # check and get product
        product = db.query(Product).filter(Product.product_id == sale_product.product_id).first()
        sale_price = product.unit_price * 1.1
        # insert the saleproduct
        stmt = insert(SaleProductAssociation).values(
            sale_id=db_sale.sale_id,
            product_id=sale_product.product_id,
            quantity=sale_product.quantity,
            unit_price=sale_price
        )
        db.execute(stmt)
        
    db.commit()
    return db_sale


def get_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sale).offset(skip).limit(limit).all()

def get_saleproduct(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SaleProductAssociation).offset(skip).limit(limit).all()