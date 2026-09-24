from fastapi import APIRouter, HTTPException

from schemas.order_schema import (
    OrderItemCreate,
    OrderItemUpdate
)

from services.order_service import OrderItemService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/orders/{order_id}/items")
def create_order_item(
    order_id: int,
    item: OrderItemCreate
):
    try:
        return OrderItemService.create_order_item(
            order_id,
            item
        )
    except Exception as error:
        handle_error(error)


@router.get("/orders/{order_id}/items")
def get_order_items(order_id: int):
    try:
        return OrderItemService.get_order_items(order_id)
    except Exception as error:
        handle_error(error)


@router.put("/orders/{order_id}/items/{item_id}")
def update_order_item(
    order_id: int,
    item_id: int,
    item: OrderItemUpdate
):
    try:
        return OrderItemService.update_order_item(
            order_id,
            item_id,
            item
        )
    except Exception as error:
        handle_error(error)


@router.delete("/orders/{order_id}/items/{item_id}")
def delete_order_item(
    order_id: int,
    item_id: int
):
    try:
        return OrderItemService.delete_order_item(
            order_id,
            item_id
        )
    except Exception as error:
        handle_error(error)


@router.post("/orders/{order_id}/recalculate")
def recalculate_order(order_id: int):
    try:
        return OrderItemService.recalculate_order(order_id)
    except Exception as error:
        handle_error(error)