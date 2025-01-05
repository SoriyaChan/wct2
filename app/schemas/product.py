from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    product_name: str
    unit_price: float
    description: Optional[str] = None
    min_threshold: int
    max_threshold: int

class ProductCreate(ProductBase):
    supplier_id: int
    category_id: int

class Product(ProductBase):
    product_id: int
    supplier_id: int
    category_id: int

    class Config:
        from_attributes = True

class ProductCategoryCreate(BaseModel):
    category_name: str
    description: str

class ProductCategory(ProductCategoryCreate):
    category_id: int

    class Config:
        from_attributes = True

class Product_Inventory(BaseModel):
    product_inventory_id: int
    product_id: int
    stock: int
    last_updated: datetime

    class Config:
        from_attributes = True