from datetime import date, datetime, time

from pydantic import BaseModel, Field


class ReservationCreate(BaseModel):
    customer_id: str
    table_id: str
    reservation_date: date
    start_time: time
    end_time: time
    guest_count: int = Field(gt=0)
    contact_number: str = Field(min_length=10, max_length=15)


class ReservationUpdate(BaseModel):
    reservation_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    guest_count: int | None = Field(default=None, gt=0)
    contact_number: str | None = None


class ReservationResponse(BaseModel):
    id: str
    customer_id: str
    table_id: str
    reservation_date: date
    start_time: time
    end_time: time
    guest_count: int
    status: str
    contact_number: str
    created_at: datetime
    updated_at: datetime