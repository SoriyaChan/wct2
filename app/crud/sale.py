from sqlalchemy.orm import Session
from sqlalchemy import insert
from ..models import Product, Sale, SaleProductAssociation, Product_Inventory, Order
from app.schemas import sale as schemas
from fastapi import HTTPException
from datetime import datetime, timedelta ,timezone
from app.crud import order
from app.schemas import order as orderschemas

SEAsia = timezone(timedelta(hours=7))

def get_low_stock_products(db: Session, skip: int = 0, limit: int = 100):
    # query all product inventories
    product_inventories = db.query(Product_Inventory).offset(skip).limit(limit).all()

    low_stock_products = []
    for inventory in product_inventories:
        product = db.query(Product).filter(Product.product_id == inventory.product_id).first()
        # if inventory under min threshold, append those product
        if inventory.stock < product.min_threshold:
            low_stock_product = orderschemas.OrderProductCreate(
                product_id=inventory.product_id,
                quantity=int((product.max_threshold - inventory.stock) / 2)
            )
            low_stock_products.append(low_stock_product)
    
    # return a list of product that need to reorder
    return low_stock_products

    
def create_sale(db: Session, sale: schemas.SaleCreate):
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
        
    # check for low stock and reorder
    low_stock_products = get_low_stock_products(db=db)
    if low_stock_products:
        order_data = orderschemas.OrderCreate(products=low_stock_products)
        order.create_order(db=db, order=order_data)

    db.commit()
    return db_sale


def get_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sale).offset(skip).limit(limit).all()

def get_saleproduct(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SaleProductAssociation).offset(skip).limit(limit).all()