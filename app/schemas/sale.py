from pydantic import BaseModel
from datetime import datetime
from typing import List

class SaleProductCreate(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(BaseModel):
    products: List[SaleProductCreate]

class SaleProductAssociation(SaleProductCreate):
    id: int
    price_at_sale: int

    class Config:
        from_attributes = True

class Sale(BaseModel):
    id: int
    sold_by: str
    total_price: int
    transaction_date: datetime

    class Config:
        from_attributes = True