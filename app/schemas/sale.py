from pydantic import BaseModel
from datetime import datetime

class SaleBase(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    sold_by: str
    total_price: int
    transaction_date: datetime

    class Config:
        from_attributes = True