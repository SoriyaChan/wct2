from pydantic import BaseModel
from datetime import datetime
from typing import List

class SaleProductCreate(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(BaseModel):
    products: List[SaleProductCreate]

class SaleProductAssociation(SaleProductCreate):
    sale_id: int
    unit_price: float

    class Config:
        from_attributes = True

class Sale(BaseModel):
    sale_id: int
    total_price: float
    sale_date: datetime

    class Config:
        from_attributes = True