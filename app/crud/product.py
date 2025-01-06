from sqlalchemy.orm import Session
from ..models import Product, Supplier, Product_Inventory, Product_Category, User
from app.schemas import product as schemas
from fastapi import HTTPException, Header

def create_product(db: Session, product: schemas.ProductCreate, api_key: str = Header(...)):
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create product")
    # query there is an existing supplier 
    supplier_id = db.query(Supplier).filter(Supplier.supplier_id == product.supplier_id).first()
    # if none
    if supplier_id is None:
        raise HTTPException(status_code=404, detail="Supplier not found") 
    # add product
    db_product = Product(
        product_name=product.product_name,
        unit_price=product.unit_price,
        description=product.description,
        min_threshold=product.min_threshold,
        max_threshold=product.max_threshold,
        supplier_id=product.supplier_id,
        category_id=product.category_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    # query product id
    product = db.query(Product).filter(Product.product_id == product_id).first()
    # if none
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def update_product(db: Session, product_id: int, updated_product: schemas.ProductCreate, api_key: str = Header(...)):
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update product")
    # query product id
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    # if none
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # query existing supplier
    supplier_id = db.query(Supplier).filter(Supplier.supplier_id == updated_product.supplier_id).first()
    # if none
    if supplier_id is None:
        raise HTTPException(status_code=404, detail="Supplier not found") 
    # update
    db_product.product_name = updated_product.product_name
    db_product.unit_price = updated_product.unit_price
    db_product.description = updated_product.description
    db_product.min_threshold = updated_product.min_threshold
    db_product.max_threshold = updated_product.max_threshold
    db_product.supplier_id = updated_product.supplier_id
    db_product.category_id = updated_product.category_id
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int, api_key: str = Header(...)):
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update product")
    # query product id
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    # if none
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # delete
    db.delete(db_product)
    db.commit()
    return db_product

def get_product_stock(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product_Inventory).offset(skip).limit(limit).all()

def create_product_category(db: Session, category: schemas.ProductCategoryCreate, api_key: str = Header(...)):
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create product")
    # query existing name
    existing_category = db.query(Product_Category).filter(Product_Category.category_name == category.category_name).first()
    # if there is 
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    # add new category
    new_category = Product_Category(
        category_name=category.category_name,
        description=category.description
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def get_product_category(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product_Category).offset(skip).limit(limit).all()