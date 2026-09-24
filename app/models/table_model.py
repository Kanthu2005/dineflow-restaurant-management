from datetime import datetime
from pydantic import BaseModel


class RestaurantTableModel(BaseModel):
    table_number: str
    capacity: int
    location: str | None = None
    status: str
    is_active: bool = True