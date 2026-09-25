from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.order_schema import (
    OrderCreate,
    OrderItemCreate,
    OrderItemUpdate,
    OrderStatusUpdate,
    OrderDiscountUpdate,
)
from app.services.order_service import OrderService, OrderItemService
from app.routes.dependencies import handle_error, get_current_user, require_roles

router = APIRouter(tags=["Orders"])


@router.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    data: OrderCreate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "WAITER", "CASHIER")),
):
    try:
        return OrderService.create_order(data)
    except Exception as e:
        handle_error(e)


@router.get("/orders/number/{order_number}")
def get_order_by_number(
    order_number: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "WAITER", "CASHIER")),
):
    try:
        return OrderService.get_order_by_number(
            order_number
        )
    except Exception as e:
        handle_error(e)


@router.get("/orders")
def get_orders(
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "WAITER", "CASHIER")),
):
    try:
        return OrderService.get_orders()
    except Exception as e:
        handle_error(e)


@router.get("/orders/{order_id}")
def get_order(
    order_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "WAITER", "CASHIER")),
):
    try:
        return OrderService.get_order(order_id)
    except Exception as e:
        handle_error(e)


@router.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: str,
    data: OrderStatusUpdate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "WAITER", "CASHIER")),
):
    try:
        return OrderService.update_status(
            order_id,
            data.status,
        )
    except Exception as e:
        handle_error(e)


@router.patch("/orders/{order_id}/discount")
def update_order_discount(
    order_id: str,
    data: OrderDiscountUpdate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "WAITER", "CASHIER")),
):
    try:
        return OrderService.update_discount(
            order_id,
            data,
        )
    except Exception as e:
        handle_error(e)


@router.post(
    "/orders/{order_id}/items",
    status_code=status.HTTP_201_CREATED,
)
def add_order_item(
    order_id: str,
    data: OrderItemCreate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "WAITER", "CASHIER")),
):
    try:
        return OrderItemService.add_item(
            order_id,
            data,
        )
    except Exception as e:
        handle_error(e)


@router.get("/orders/{order_id}/items")
def get_order_items(
    order_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "WAITER", "CASHIER")),
):
    try:
        return OrderItemService.get_order_items(
            order_id
        )
    except Exception as e:
        handle_error(e)


@router.put("/orders/{order_id}/items/{item_id}")
def update_order_item(
    order_id: str,
    item_id: str,
    data: OrderItemUpdate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "WAITER", "CASHIER")),
):
    try:
        return OrderItemService.update_item(
            order_id,
            item_id,
            data,
        )
    except Exception as e:
        handle_error(e)


@router.delete("/orders/{order_id}/items/{item_id}")
def delete_order_item(
    order_id: str,
    item_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "WAITER", "CASHIER")),
):
    try:
        return OrderItemService.delete_item(
            order_id,
            item_id,
        )
    except Exception as e:
        handle_error(e)


@router.post("/orders/{order_id}/recalculate")
def recalculate_order(
    order_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "WAITER", "CASHIER")),
):
    try:
        return OrderItemService.recalculate_order(
            order_id
        )
    except Exception as e:
        handle_error(e)
