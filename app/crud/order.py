from sqlalchemy.orm import Session
from sqlalchemy import insert
from ..models import Product, Order, OrderProductAssociation, Product_Inventory
from app.schemas import order as schemas
from fastapi import HTTPException
from datetime import datetime, timedelta ,timezone

SEAsia = timezone(timedelta(hours=7))

def create_order(db: Session, order: schemas.OrderCreate):
    total_price = 0
    # loop product in products
    for order_product in order.products:
        # check and get product
        product = db.query(Product).filter(Product.product_id == order_product.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {order_product.product_id} not found.")
        # if exist add its price to the total price
        total_price += order_product.quantity * product.unit_price
    # add an order
    db_order = Order(
        total_price=total_price,
        order_date=datetime.now(SEAsia)
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    # loop product in products
    for order_product in order.products:
        # check and get product
        product = db.query(Product).filter(Product.product_id == order_product.product_id).first()
        # insert the orderproduct 
        stmt = insert(OrderProductAssociation).values(
            order_id=db_order.order_id,
            product_id=order_product.product_id,
            quantity=order_product.quantity,
            unit_price=product.unit_price
        )
        db.execute(stmt)
        # get product stock
        product_stock = db.query(Product_Inventory).filter(Product_Inventory.product_id == order_product.product_id).first()
        # if there is, increment and change date
        if product_stock:
            product_stock.stock += order_product.quantity
            product_stock.last_updated=datetime.now(SEAsia)
            db.commit()
            db.refresh(product_stock)
        # if there isn't, add a new product stock
        else: 
            db_stock = Product_Inventory(
                product_id=order_product.product_id,
                stock=order_product.quantity,
                last_updated=datetime.now(SEAsia)
            )
            db.add(db_stock)
            db.commit()

    db.commit()
    return db_order


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()

def get_orderproduct(db: Session, skip: int = 0, limit: int = 100):
    return db.query(OrderProductAssociation).offset(skip).limit(limit).all()