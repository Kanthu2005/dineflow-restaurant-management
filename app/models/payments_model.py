from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class InvoiceModel(BaseModel):
    order_id: str
    invoice_number: str
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    status: str
    generated_at: datetime


class PaymentModel(BaseModel):
    invoice_id: str
    amount: Decimal
    payment_method: str
    payment_status: str
    transaction_reference: str | None = None
    paid_at: datetime | None = None
    recorded_by: str


class RefundModel(BaseModel):
    payment_id: str
    order_id: str
    requested_amount: Decimal
    approved_amount: Decimal
    reason: str
    status: str
    approved_by: str | None = None
    processed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime