from datetime import datetime
<<<<<<< HEAD

from pydantic import BaseModel


class FeedbackModel(BaseModel):
    order_id: str
    customer_id: str
    rating: int
    food_rating: int
    service_rating: int
    comments: str | None = None
    created_at: datetime
=======
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict


class FeedbackModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    id: Optional[ObjectId] = None

    order_id: ObjectId
    customer_id: ObjectId

    rating: int = Field(..., ge=1, le=5)
    food_rating: int = Field(..., ge=1, le=5)
    service_rating: int = Field(..., ge=1, le=5)

    comments: Optional[str] = None
    created_at: Optional[datetime] = None
>>>>>>> main
