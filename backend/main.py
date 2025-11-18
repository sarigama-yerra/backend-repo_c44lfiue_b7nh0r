from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os

from schemas import Product, Order
from database import create_document, get_documents, get_document_by_id

app = FastAPI(title="E-commerce COD API")

# CORS
frontend_url = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
async def test():
    return {"status": "ok"}


# Products Endpoints
@app.get("/products", response_model=List[Product])
async def list_products(category: Optional[str] = None):
    filter_q = {"category": category} if category else {}
    docs = await get_documents("product", filter_q)
    return docs


@app.get("/products/{product_id}", response_model=Optional[Product])
async def get_product(product_id: str):
    doc = await get_document_by_id("product", product_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")
    return doc


@app.post("/products", response_model=Product)
async def create_product(payload: Product):
    doc = await create_document("product", payload.model_dump())
    return doc


# Orders Endpoints
class OrderResponse(BaseModel):
    id: str
    message: str


@app.post("/orders", response_model=OrderResponse)
async def create_order(order: Order):
    # Save order to DB
    saved = await create_document("order", order.model_dump())

    # Send email (placeholder: prints to logs). In real life, integrate email provider.
    placeholder_email = os.getenv("ORDERS_EMAIL", "owner@example.com")
    print(f"Send order email to {placeholder_email}: {saved}")

    return OrderResponse(id=saved.get("id", ""), message="Your COD Order is Confirmed")
