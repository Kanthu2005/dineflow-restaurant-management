<<<<<<< HEAD
from datetime import datetime

from pydantic import BaseModel


class KitchenTicketModel(BaseModel):
    order_id: str
    status: str
    priority: str = "NORMAL"
    assigned_staff_id: str | None = None
    started_at: datetime | None = None
    ready_at: datetime | None = None
    completed_at: datetime | None = None


class KitchenTicketItemModel(BaseModel):
    kitchen_ticket_id: str
    order_item_id: str
    station: str
    status: str


class StaffAssignmentModel(BaseModel):
    kitchen_ticket_id: str
    staff_id: str
    assigned_at: datetime
    unassigned_at: datetime | None = None


class PreparationEstimateModel(BaseModel):
    order_id: str
    estimated_minutes: int
    estimated_ready_time: datetime
    calculation_basis: str
=======
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class KitchenTicketCreate(BaseModel):
    order_id: str
    priority: str = "NORMAL"

class KitchenStaffAssignment(BaseModel):
    staff_id: str

class KitchenTicket(BaseModel):
    id: str
    order_id: str
    status: str
    priority: str
    assigned_staff_id: Optional[str] = None
    started_at: Optional[datetime] = None
    ready_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
>>>>>>> main
