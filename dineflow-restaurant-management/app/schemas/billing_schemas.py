from pydantic import BaseModel, Field, root_validator
from typing import Optional
from datetime import datetime


class GenerateBill(BaseModel):
    order_id: int
    discount_amount: float = 0.0
    tax_percent: float = 5.0


class BillItem(BaseModel):
    menu_item_id: int
    name: str
    quantity: int
    unit_price: float
    total: Optional[float] = None

    @root_validator
    def compute_total(cls, values):
        qty = values.get("quantity")
        price = values.get("unit_price")
        if qty is not None and price is not None:
            values["total"] = round(qty * price, 2)
        return values


class BillSummary(BaseModel):
    bill_id: int
    order_id: int
    subtotal: float
    tax_amount: float
    discount_amount: float
    grand_total: float
    generated_at: datetime
    is_paid: bool = False


class UpdateBillDiscount(BaseModel):
    discount_amount: float = Field(ge=0)
    reason: Optional[str] = None


