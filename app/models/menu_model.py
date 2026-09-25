<<<<<<< HEAD
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
=======
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class MenuCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class MenuCategoryCreate(MenuCategoryBase):
    pass

class MenuCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class MenuCategory(MenuCategoryBase):
    id: str
    created_at: datetime


class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
>>>>>>> main
    category_id: str
    price: Decimal
    preparation_time: int
    is_available: bool = True
    is_vegetarian: bool = False
<<<<<<< HEAD
    created_at: datetime
=======

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    price: Optional[Decimal] = None
    preparation_time: Optional[int] = None
    is_available: Optional[bool] = None
    is_vegetarian: Optional[bool] = None

class MenuItem(MenuItemBase):
    id: str
    created_at: datetime
>>>>>>> main
