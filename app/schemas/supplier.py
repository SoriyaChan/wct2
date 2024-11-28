from pydantic import BaseModel
from typing import List
from .product import Product

class SupplierBase(BaseModel):
    name: str
    address: str
    phone: str

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int
    created_by: str
    products: List[Product] = []

    class Config:
        from_attributes = True
