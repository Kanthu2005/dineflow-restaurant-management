from fastapi import APIRouter, HTTPException

from schemas.kitchen_schema import (
    KitchenTicketCreate,
    KitchenStaffAssignment,
    OrderStatusUpdate
)

from services.kitchen_service import KitchenService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/kitchen/tickets")
def create_kitchen_ticket(ticket: KitchenTicketCreate):
    try:
        return KitchenService.create_ticket(ticket)
    except Exception as error:
        handle_error(error)


@router.get("/kitchen/tickets/{ticket_id}")
def get_kitchen_ticket(ticket_id: int):
    try:
        return KitchenService.get_ticket(ticket_id)
    except Exception as error:
        handle_error(error)


@router.patch("/kitchen/tickets/{ticket_id}/status")
def update_ticket_status(
    ticket_id: int,
    status: OrderStatusUpdate
):
    try:
        return KitchenService.update_ticket_status(
            ticket_id,
            status
        )
    except Exception as error:
        handle_error(error)


@router.post("/kitchen/tickets/{ticket_id}/assign")
def assign_kitchen_staff(
    ticket_id: int,
    assignment: KitchenStaffAssignment
):
    try:
        return KitchenService.assign_staff(
            ticket_id,
            assignment
        )
    except Exception as error:
        handle_error(error)