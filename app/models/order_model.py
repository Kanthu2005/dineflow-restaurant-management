<<<<<<< HEAD
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
=======
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class OrderBase(BaseModel):
    customer_id: Optional[str] = None
    table_id: Optional[str] = None
    order_type: str
    created_by: str

class OrderCreate(OrderBase):
    pass

class OrderStatusUpdate(BaseModel):
    status: str

class OrderDiscountUpdate(BaseModel):
    discount: Decimal

class Order(OrderBase):
    id: str
    order_number: str
>>>>>>> main
    status: str
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
<<<<<<< HEAD
    created_by: str
    created_at: datetime
=======
    created_at: datetime
>>>>>>> main
