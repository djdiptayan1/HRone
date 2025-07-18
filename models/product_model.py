from pydantic import BaseModel
from typing import List, Optional


class SizeQuantity(BaseModel):
    size: str
    quantity: int


class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[SizeQuantity]


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float


class OrderProductResponse(BaseModel):
    id: str
    name: str


class ProductDB(ProductCreate):
    id: str
