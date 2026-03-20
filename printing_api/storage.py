from typing import Dict, List, Optional
from uuid import uuid4, UUID
from .models import Order, OrderCreate
from datetime import datetime
import json
import os

# Simple in-memory store. Keys are string UUIDs, values are dict serializable by pydantic
STORE: Dict[str, dict] = {}

# Optional persistence file. If environment variable PRINTING_API_PERSIST is set to a filepath,
# the store will be saved to that file on each create and loaded at startup.
PERSIST_FILE = os.getenv("PRINTING_API_PERSIST", "")


def _calc_total(order_create: OrderCreate) -> float:
    return sum(i.quantity * i.unit_price for i in order_create.items)


def create_order(order_create: OrderCreate) -> Order:
    oid = uuid4()
    total = _calc_total(order_create)
    order = Order(
        id=oid,
        customer_name=order_create.customer_name,
        items=order_create.items,
        total=round(total, 2),
        created_at=datetime.utcnow(),
    )
    STORE[str(oid)] = order.dict()
    if PERSIST_FILE:
        _save()
    return order


def list_orders() -> List[Order]:
    return [Order(**v) for v in STORE.values()]


def get_order(order_id: str) -> Optional[Order]:
    v = STORE.get(order_id)
    if not v:
        return None
    return Order(**v)


def _save():
    try:
        with open(PERSIST_FILE, "w") as f:
            json.dump(list(STORE.values()), f, default=str)
    except Exception:
        # Keep fail-safe: persistence is optional
        pass


def _load():
    if PERSIST_FILE and os.path.exists(PERSIST_FILE):
        try:
            with open(PERSIST_FILE, "r") as f:
                arr = json.load(f)
                for o in arr:
                    STORE[o["id"]] = o
        except Exception:
            # ignore parse/load errors for prototype
            pass


# Load persisted orders (if configured) when module is imported
_load()
