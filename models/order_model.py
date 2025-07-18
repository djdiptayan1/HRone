from pydantic import BaseModel
from typing import List
from models.product_model import OrderProductResponse


class OrderItem(BaseModel):
    productId: str
    qty: int


class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]


class OrderItemResponse(BaseModel):
    productDetails: OrderProductResponse
    qty: int


class OrderResponse(BaseModel):
    id: str
    items: List[OrderItemResponse]
    total: float
