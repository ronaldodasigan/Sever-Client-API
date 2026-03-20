from pydantic import BaseModel, Field
from typing import List
from uuid import UUID
from datetime import datetime


class Item(BaseModel):
    name: str
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., ge=0.0)


class OrderCreate(BaseModel):
    customer_name: str
    items: List[Item]


class Order(OrderCreate):
    id: UUID
    total: float
    created_at: datetime
