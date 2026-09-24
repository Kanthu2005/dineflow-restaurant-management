from decimal import Decimal
from pydantic import BaseModel


class RecipeModel(BaseModel):
    menu_item_id: str
    ingredient_id: str
    quantity_required: Decimal