from fastapi import APIRouter, HTTPException

from services.activity_log_service import ActivityLogService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/orders/{order_id}/activity")
def create_activity(order_id: int):
    try:
        return ActivityLogService.create_activity(order_id)
    except Exception as error:
        handle_error(error)


@router.get("/orders/{order_id}/activity")
def get_activity(order_id: int):
    try:
        return ActivityLogService.get_activity(order_id)
    except Exception as error:
        handle_error(error)