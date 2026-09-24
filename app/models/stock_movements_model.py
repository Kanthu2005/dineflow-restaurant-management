from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class StockMovementModel(BaseModel):
    ingredient_id: str
    movement_type: str
    quantity: Decimal
    reference_type: str | None = None
    reference_id: str | None = None
    created_by: str
    created_at: datetime