from datetime import datetime

from pydantic import BaseModel


class FeedbackModel(BaseModel):
    order_id: str
    customer_id: str
    rating: int
    food_rating: int
    service_rating: int
    comments: str | None = None
    created_at: datetime