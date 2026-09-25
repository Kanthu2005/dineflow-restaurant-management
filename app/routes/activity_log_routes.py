from fastapi import APIRouter, Depends, HTTPException, status
from app.services.activity_log_service import ActivityLogService
from app.routes.dependencies import handle_error, get_current_user, require_roles

router = APIRouter(tags=["Activity Logs"])


@router.post(
    "/orders/{order_id}/activity",
    status_code=status.HTTP_201_CREATED,
)
def create_activity_log(
    order_id: str,
    data: dict,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER")),
):
    try:
        if not data.get("action"):
            raise ValueError("action is required")

        return ActivityLogService.create_log(
            order_id=order_id,
            action=data["action"],
            performed_by=data.get("performed_by") or current_user.get("id"),
            details=data.get("details"),
        )
    except Exception as e:
        handle_error(e)


@router.get("/orders/{order_id}/activity")
def get_order_activity(
    order_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER")),
):
    try:
        return ActivityLogService.get_order_logs(order_id)
    except Exception as e:
        handle_error(e)
