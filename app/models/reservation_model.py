from datetime import date, datetime, time
from pydantic import BaseModel


class ReservationModel(BaseModel):
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