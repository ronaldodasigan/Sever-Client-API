from fastapi import FastAPI, HTTPException
from .models import OrderCreate
from . import storage
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Ronaldo's School Supply API",
    description="Prototype per PRD: FastAPI backend, in-memory store",
)

# Allow all origins for the prototype (adjust in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Ronaldo's Printing Shop - FastAPI prototype."}


@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):
    created = storage.create_order(order)
    return created


@app.get("/orders")
def list_orders():
    return storage.list_orders()


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    ord = storage.get_order(order_id)
    if not ord:
        raise HTTPException(status_code=404, detail="Order not found")
    return ord
