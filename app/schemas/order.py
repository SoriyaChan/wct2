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
    unit_price: float

    class Config:
        from_attributes = True

class Order(BaseModel):
    order_id: int
    total_price: float
    order_date: datetime

    class Config:
        from_attributes = True