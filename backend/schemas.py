from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class Product(BaseModel):
    title: str
    description: str
    price: float
    category: str
    images: List[str] = []
    features: Optional[List[str]] = []
    benefits: Optional[List[str]] = []
    specifications: Optional[List[str]] = []
    discount_percent: Optional[float] = 0


class Order(BaseModel):
    product_id: str
    product_title: str
    quantity: int = Field(ge=1, default=1)
    full_name: str
    mobile: str
    address: str
    city: str
    state: str
    pincode: str
    email: Optional[EmailStr] = None
