from fastapi import APIRouter, HTTPException

from schemas.kitchen_event_schema import KitchenEventCreate
from services.kitchen_event_service import KitchenEventService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/kitchen/events")
def create_kitchen_event(event: KitchenEventCreate):
    try:
        return KitchenEventService.create_event(event)
    except Exception as error:
        handle_error(error)


@router.get("/kitchen/events/order/{order_id}")
def get_order_kitchen_events(order_id: int):
    try:
        return KitchenEventService.get_order_events(order_id)
    except Exception as error:
        handle_error(error)