from fastapi import APIRouter, HTTPException

from schemas.feedback_schema import FeedbackCreate
from services.feedback_service import FeedbackService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/orders/{order_id}/feedback")
def create_feedback(
    order_id: int,
    feedback: FeedbackCreate
):
    try:
        return FeedbackService.create_feedback(
            order_id,
            feedback
        )
    except Exception as error:
        handle_error(error)


@router.get("/feedback/{feedback_id}")
def get_feedback(feedback_id: int):
    try:
        return FeedbackService.get_feedback(feedback_id)
    except Exception as error:
        handle_error(error)


@router.get("/feedback/customer/{customer_id}")
def get_customer_feedback(customer_id: int):
    try:
        return FeedbackService.get_customer_feedback(customer_id)
    except Exception as error:
        handle_error(error)


@router.get("/feedback/order/{order_id}")
def get_order_feedback(order_id: int):
    try:
        return FeedbackService.get_order_feedback(order_id)
    except Exception as error:
        handle_error(error)


@router.get("/feedback/summary")
def get_feedback_summary():
    try:
        return FeedbackService.get_feedback_summary()
    except Exception as error:
        handle_error(error)


@router.get("/feedback")
def get_feedbacks():
    try:
        return FeedbackService.get_feedbacks()
    except Exception as error:
        handle_error(error)