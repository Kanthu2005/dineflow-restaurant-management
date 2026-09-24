from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class MenuCategoryModel(BaseModel):
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime


class MenuItemModel(BaseModel):
    name: str
    description: str | None = None
    category_id: str
    price: Decimal
    preparation_time: int
    is_available: bool = True
    is_vegetarian: bool = False
    created_at: datetime