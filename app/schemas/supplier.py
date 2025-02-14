from pydantic import BaseModel
from typing import List
from .product import Product

class SupplierBase(BaseModel):
    supplier_name: str
    address: str
    phone: str

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    supplier_id: int
    products: List[Product] = []

    class Config:
        from_attributes = True
