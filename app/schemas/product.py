from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    product_name: str
    unit_price: int
    description: Optional[str] = None

class ProductCreate(ProductBase):
    supplier_id: int

class Product(ProductBase):
    product_id: int
    created_by: str
    supplier_id: int

    class Config:
        from_attributes = True

class Product_Inventory(BaseModel):
    product_inventory_id: int
    product_id: int
    stock: int
    last_updated: datetime

    class Config:
        from_attributes = True