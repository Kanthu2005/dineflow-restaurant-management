from datetime import datetime

from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    customer_id: str
    rating: int = Field(ge=1, le=5)
    food_rating: int = Field(ge=1, le=5)
    service_rating: int = Field(ge=1, le=5)
    comments: str | None = Field(default=None, max_length=1000)


class FeedbackResponse(BaseModel):
    id: str
    order_id: str
    customer_id: str
    rating: int
    food_rating: int
    service_rating: int
    comments: str | None = None
    created_at: datetime


class FeedbackSummaryResponse(BaseModel):
    total_feedback: int
    average_rating: float
    average_food_rating: float
    average_service_rating: float