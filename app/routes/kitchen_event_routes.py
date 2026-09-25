from fastapi import APIRouter, Depends, HTTPException, status
from app.services.kitchen_event_service import KitchenEventService
from app.routes.dependencies import handle_error, get_current_user, require_roles

router = APIRouter(tags=["Kitchen Events"])


@router.post(
    "/kitchen/events",
    status_code=status.HTTP_201_CREATED,
)
def create_kitchen_event(
    data: dict,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF")),
):
    try:
        if not data.get("order_id"):
            raise ValueError("order_id is required")

        if not data.get("event_type"):
            raise ValueError("event_type is required")

        return KitchenEventService.create_event(
            order_id=data["order_id"],
            event_type=data["event_type"],
            kitchen_ticket_id=data.get("kitchen_ticket_id"),
            details=data.get("details"),
        )
    except Exception as e:
        handle_error(e)


@router.get("/kitchen/events/order/{order_id}")
def get_order_kitchen_events(
    order_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF")),
):
    try:
        return KitchenEventService.get_order_events(order_id)
    except Exception as e:
        handle_error(e)
