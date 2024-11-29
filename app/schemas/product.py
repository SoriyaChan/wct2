from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: int
    stock: int
    description: Optional[str] = None

class ProductCreate(ProductBase):
    supplier_id: int

class Product(ProductBase):
    id: int
    created_by: str
    supplier_id: int

    class Config:
        from_attributes = True
