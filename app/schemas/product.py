from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: int
    description: Optional[str] = None

class ProductCreate(ProductBase):
    supplier_id: int

class Product(ProductBase):
    id: int
    supplier_id: int

    class Config:
        orm_mode = True
