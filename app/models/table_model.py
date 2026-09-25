<<<<<<< HEAD
from datetime import datetime
from pydantic import BaseModel


class RestaurantTableModel(BaseModel):
    table_number: str
    capacity: int
    location: str | None = None
    status: str
    is_active: bool = True
=======
from pydantic import BaseModel
from typing import Optional

class RestaurantTableBase(BaseModel):
    table_number: int
    capacity: int
    location: Optional[str] = None
    is_active: bool = True
    status: str = "AVAILABLE"

class RestaurantTableCreate(RestaurantTableBase):
    pass

class RestaurantTableUpdate(BaseModel):
    table_number: Optional[int] = None
    capacity: Optional[int] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None
    status: Optional[str] = None

class RestaurantTable(RestaurantTableBase):
    id: str
>>>>>>> main
