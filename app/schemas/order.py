from pydantic import BaseModel
from datetime import datetime
from typing import List

class OrderProductCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    products: List[OrderProductCreate]

class OrderProductAssociation(OrderProductCreate):
    order_id: int
    unit_price: int

    class Config:
        from_attributes = True

class Order(BaseModel):
    order_id: int
    order_by: str
    total_price: int
    order_date: datetime

    class Config:
        from_attributes = True