from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.kitchen_schema import (
    KitchenTicketCreate,
    KitchenStaffAssignment,
)
from app.services.kitchen_service import KitchenService
from app.routes.dependencies import handle_error, get_current_user, require_roles

router = APIRouter(tags=["Kitchen"])


@router.post(
    "/kitchen/tickets",
    status_code=status.HTTP_201_CREATED,
)
def create_kitchen_ticket(
    data: KitchenTicketCreate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF", "WAITER")),
):
    try:
        return KitchenService.create_ticket(
            data.order_id,
            data.priority,
        )
    except Exception as e:
        handle_error(e)


@router.get("/kitchen/tickets")
def get_kitchen_tickets(
    status: str = None,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF", "WAITER")),
):
    try:
        return KitchenService.get_tickets(status)
    except Exception as e:
        handle_error(e)


@router.get("/kitchen/tickets/{ticket_id}")
def get_kitchen_ticket(
    ticket_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF", "WAITER")),
):
    try:
        return KitchenService.get_ticket(ticket_id)
    except Exception as e:
        handle_error(e)


@router.patch("/kitchen/tickets/{ticket_id}/status")
def update_ticket_status(
    ticket_id: str,
    status_value: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF", "WAITER")),
):
    try:
        return KitchenService.update_ticket_status(
            ticket_id,
            status_value,
        )
    except Exception as e:
        handle_error(e)


@router.post(
    "/kitchen/tickets/{ticket_id}/assign",
    status_code=status.HTTP_200_OK,
)
def assign_kitchen_staff(
    ticket_id: str,
    data: KitchenStaffAssignment,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF")),
):
    try:
        return KitchenService.assign_staff(
            ticket_id,
            data.user_id,
            data.role,
        )
    except Exception as e:
        handle_error(e)
