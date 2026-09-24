from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class OrderItemModel(BaseModel):
    order_id: str
    menu_item_id: str
    item_name_snapshot: str
    unit_price_snapshot: Decimal
    quantity: int
    special_instructions: str | None = None
    item_total: Decimal


class OrderModel(BaseModel):
    order_number: str
    customer_id: str | None = None
    table_id: str | None = None
    order_type: str
    status: str
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    created_by: str
    created_at: datetime