from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class IngredientModel(BaseModel):
    name: str
    unit: str
    available_quantity: Decimal
    minimum_stock_level: Decimal
    cost_per_unit: Decimal
    supplier_name: str | None = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime