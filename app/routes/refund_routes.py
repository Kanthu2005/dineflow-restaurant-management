from fastapi import APIRouter, HTTPException

from schemas.refund_schema import (
    RefundCreate,
    RefundApproval
)

from services.refund_service import RefundService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/refunds")
def create_refund(refund: RefundCreate):
    try:
        return RefundService.create_refund(refund)
    except Exception as error:
        handle_error(error)


@router.patch("/refunds/{refund_id}/approve")
def approve_refund(
    refund_id: int,
    approval: RefundApproval
):
    try:
        return RefundService.approve_refund(
            refund_id,
            approval
        )
    except Exception as error:
        handle_error(error)


@router.get("/refunds/order/{order_id}")
def get_order_refunds(order_id: int):
    try:
        return RefundService.get_order_refunds(order_id)
    except Exception as error:
        handle_error(error)


@router.get("/refunds/{refund_id}")
def get_refund(refund_id: int):
    try:
        return RefundService.get_refund(refund_id)
    except Exception as error:
        handle_error(error)