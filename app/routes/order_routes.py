from fastapi import APIRouter, HTTPException

from schemas.order_schema import (
    OrderCreate,
    OrderStatusUpdate,
    OrderDiscountUpdate
)

from services.order_service import OrderService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/orders")
def create_order(order: OrderCreate):
    try:
        return OrderService.create_order(order)
    except Exception as error:
        handle_error(error)


@router.get("/orders/number/{order_number}")
def get_order_by_number(order_number: str):
    try:
        return OrderService.get_order_by_number(order_number)
    except Exception as error:
        handle_error(error)


@router.get("/orders")
def get_orders():
    try:
        return OrderService.get_orders()
    except Exception as error:
        handle_error(error)


@router.get("/orders/{order_id}")
def get_order(order_id: int):
    try:
        return OrderService.get_order(order_id)
    except Exception as error:
        handle_error(error)


@router.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status: OrderStatusUpdate
):
    try:
        return OrderService.update_order_status(
            order_id,
            status
        )
    except Exception as error:
        handle_error(error)


@router.patch("/orders/{order_id}/discount")
def update_order_discount(
    order_id: int,
    discount: OrderDiscountUpdate
):
    try:
        return OrderService.update_order_discount(
            order_id,
            discount
        )
    except Exception as error:
        handle_error(error)