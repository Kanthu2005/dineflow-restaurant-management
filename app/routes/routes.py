<<<<<<< HEAD
from fastapi import APIRouter, HTTPException, status

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
)

from app.schemas.customer_schema import (
    CustomerCreate,
    CustomerUpdate,
)

from app.schemas.menu_schema import (
    MenuCategoryCreate,
    MenuCategoryUpdate,
    MenuItemCreate,
    MenuItemUpdate,
)

from app.schemas.recipe_schema import (
    RecipeCreate,
    RecipeUpdate,
)

from app.schemas.ingredient_schema import (
    IngredientCreate,
    IngredientUpdate,
    StockUpdate,
)

from app.schemas.table_schema import (
    RestaurantTableCreate,
    RestaurantTableUpdate,
    TableStatusUpdate,
)

from app.schemas.reservation_schema import (
    ReservationCreate,
    ReservationUpdate,
)

from app.schemas.order_schema import (
    OrderCreate,
    OrderItemCreate,
    OrderItemUpdate,
    OrderStatusUpdate,
    OrderDiscountUpdate,
)

from app.schemas.kitchen_schema import (
    KitchenTicketCreate,
    KitchenStaffAssignment,
)

from app.schemas.payments_schema import (
    InvoiceCreate,
    PaymentCreate,
    RefundCreate,
    RefundApproval,
)

from app.schemas.feedback_schema import (
    FeedbackCreate,
)

from app.services.service import (
    UserService,
    CustomerService,
    MenuCategoryService,
    MenuItemService,
    IngredientService,
    RecipeService,
    RestaurantTableService,
    ReservationService,
    OrderService,
    OrderItemService,
    KitchenService,
    StockMovementService,
    BillingService,
    PaymentService,
    RefundService,
    ActivityLogService,
    KitchenEventService,
    FeedbackService,
)


router = APIRouter()


def handle_error(error: Exception):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(error),
    )


# user routes

@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate):
    try:
        return UserService.create_user(data)
    except Exception as e:
        handle_error(e)


@router.get("/users")
def get_users():
    try:
        return UserService.get_users()
    except Exception as e:
        handle_error(e)


@router.get("/users/{user_id}")
def get_user(user_id: str):
    try:
        return UserService.get_user(user_id)
    except Exception as e:
        handle_error(e)


@router.put("/users/{user_id}")
def update_user(
    user_id: str,
    data: UserUpdate,
):
    try:
        return UserService.update_user(
            user_id,
            data,
        )
    except Exception as e:
        handle_error(e)


@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    try:
        return UserService.delete_user(user_id)
    except Exception as e:
        handle_error(e)


# customer routes

@router.post("/customers", status_code=status.HTTP_201_CREATED)
def create_customer(data: CustomerCreate):
    try:
        return CustomerService.create_customer(data)
    except Exception as e:
        handle_error(e)


@router.get("/customers")
def get_customers():
    try:
        return CustomerService.get_customers()
    except Exception as e:
        handle_error(e)


@router.get("/customers/{customer_id}")
def get_customer(customer_id: str):
    try:
        return CustomerService.get_customer(customer_id)
    except Exception as e:
        handle_error(e)


@router.put("/customers/{customer_id}")
def update_customer(
    customer_id: str,
    data: CustomerUpdate,
):
    try:
        return CustomerService.update_customer(
            customer_id,
            data,
        )
    except Exception as e:
        handle_error(e)


# menu category routes

@router.post(
    "/menu/categories",
    status_code=status.HTTP_201_CREATED,
)
def create_menu_category(data: MenuCategoryCreate):
    try:
        return MenuCategoryService.create_category(data)
    except Exception as e:
        handle_error(e)


@router.get("/menu/categories")
def get_menu_categories():
    try:
        return MenuCategoryService.get_categories()
    except Exception as e:
        handle_error(e)


@router.get("/menu/categories/{category_id}")
def get_menu_category(category_id: str):
    try:
        return MenuCategoryService.get_category(category_id)
    except Exception as e:
        handle_error(e)


@router.put("/menu/categories/{category_id}")
def update_menu_category(
    category_id: str,
    data: MenuCategoryUpdate,
):
    try:
        return MenuCategoryService.update_category(
            category_id,
            data,
        )
    except Exception as e:
        handle_error(e)


# menu item routes

@router.post(
    "/menu/items",
    status_code=status.HTTP_201_CREATED,
)
def create_menu_item(data: MenuItemCreate):
    try:
        return MenuItemService.create_item(data)
    except Exception as e:
        handle_error(e)


@router.get("/menu/items/available")
def get_available_menu_items():
    try:
        return MenuItemService.get_available_items()
    except Exception as e:
        handle_error(e)


@router.get("/menu/items/category/{category_id}")
def get_menu_items_by_category(category_id: str):
    try:
        return MenuItemService.get_items_by_category(category_id)
    except Exception as e:
        handle_error(e)


@router.get("/menu/items")
def get_menu_items():
    try:
        return MenuItemService.get_items()
    except Exception as e:
        handle_error(e)


@router.get("/menu/items/{item_id}")
def get_menu_item(item_id: str):
    try:
        return MenuItemService.get_item(item_id)
    except Exception as e:
        handle_error(e)


@router.put("/menu/items/{item_id}")
def update_menu_item(
    item_id: str,
    data: MenuItemUpdate,
):
    try:
        return MenuItemService.update_item(
            item_id,
            data,
        )
    except Exception as e:
        handle_error(e)


# ingredient routes

@router.post(
    "/ingredients",
    status_code=status.HTTP_201_CREATED,
)
def create_ingredient(data: IngredientCreate):
    try:
        return IngredientService.create_ingredient(data)
    except Exception as e:
        handle_error(e)


@router.get("/ingredients/active")
def get_active_ingredients():
    try:
        return IngredientService.get_active_ingredients()
    except Exception as e:
        handle_error(e)


@router.get("/ingredients")
def get_ingredients():
    try:
        return IngredientService.get_ingredients()
    except Exception as e:
        handle_error(e)


@router.get("/ingredients/{ingredient_id}")
def get_ingredient(ingredient_id: str):
    try:
        return IngredientService.get_ingredient(ingredient_id)
    except Exception as e:
        handle_error(e)


@router.put("/ingredients/{ingredient_id}")
def update_ingredient(
    ingredient_id: str,
    data: IngredientUpdate,
):
    try:
        return IngredientService.update_ingredient(
            ingredient_id,
            data,
        )
    except Exception as e:
        handle_error(e)


@router.post("/ingredients/{ingredient_id}/stock")
def update_ingredient_stock(
    ingredient_id: str,
    data: StockUpdate,
):
    try:
        return IngredientService.update_stock(
            ingredient_id,
            data.quantity,
        )
    except Exception as e:
        handle_error(e)


@router.get("/ingredients/{ingredient_id}/stock-status")
def get_stock_status(ingredient_id: str):
    try:
        return IngredientService.get_stock_status(ingredient_id)
    except Exception as e:
        handle_error(e)


# recipe routes

@router.post(
    "/menu/items/{menu_item_id}/recipes",
    status_code=status.HTTP_201_CREATED,
)
def create_recipe(
    menu_item_id: str,
    data: RecipeCreate,
):
    try:
        return RecipeService.create_recipe(
            menu_item_id,
            data,
        )
    except Exception as e:
        handle_error(e)


@router.get("/menu/items/{menu_item_id}/recipes")
def get_menu_item_recipe(menu_item_id: str):
    try:
        return RecipeService.get_recipe(menu_item_id)
    except Exception as e:
        handle_error(e)


@router.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: str):
    try:
        return RecipeService.get_recipe_by_id(recipe_id)
    except Exception as e:
        handle_error(e)


@router.put("/recipes/{recipe_id}")
def update_recipe(
    recipe_id: str,
    data: RecipeUpdate,
):
    try:
        return RecipeService.update_recipe(
            recipe_id,
            data,
        )
    except Exception as e:
        handle_error(e)


# restaurant table routes

@router.post(
    "/tables",
    status_code=status.HTTP_201_CREATED,
)
def create_table(data: RestaurantTableCreate):
    try:
        return RestaurantTableService.create_table(data)
    except Exception as e:
        handle_error(e)


@router.get("/tables/available")
def get_available_tables():
    try:
        return RestaurantTableService.get_available_tables()
    except Exception as e:
        handle_error(e)


@router.get("/tables")
def get_tables():
    try:
        return RestaurantTableService.get_tables()
    except Exception as e:
        handle_error(e)


@router.get("/tables/{table_id}")
def get_table(table_id: str):
    try:
        return RestaurantTableService.get_table(table_id)
    except Exception as e:
        handle_error(e)


@router.put("/tables/{table_id}")
def update_table(
    table_id: str,
    data: RestaurantTableUpdate,
):
    try:
        return RestaurantTableService.update_table(
            table_id,
            data,
        )
    except Exception as e:
        handle_error(e)


@router.patch("/tables/{table_id}/status")
def update_table_status(
    table_id: str,
    data: TableStatusUpdate,
):
    try:
        return RestaurantTableService.update_status(
            table_id,
            data.status,
        )
    except Exception as e:
        handle_error(e)


# reservation routes

@router.post(
    "/reservations",
    status_code=status.HTTP_201_CREATED,
)
def create_reservation(data: ReservationCreate):
    try:
        return ReservationService.create_reservation(data)
    except Exception as e:
        handle_error(e)


@router.get("/reservations")
def get_reservations():
    try:
        return ReservationService.get_reservations()
    except Exception as e:
        handle_error(e)


@router.get("/reservations/customer/{customer_id}")
def get_customer_reservations(customer_id: str):
    try:
        return ReservationService.get_by_customer(customer_id)
    except Exception as e:
        handle_error(e)


@router.get("/reservations/table/{table_id}")
def get_table_reservations(table_id: str):
    try:
        return ReservationService.get_by_table(table_id)
    except Exception as e:
        handle_error(e)


@router.get("/reservations/{reservation_id}")
def get_reservation(reservation_id: str):
    try:
        return ReservationService.get_reservation(reservation_id)
    except Exception as e:
        handle_error(e)


@router.put("/reservations/{reservation_id}")
def update_reservation(
    reservation_id: str,
    data: ReservationUpdate,
):
    try:
        return ReservationService.update_reservation(
            reservation_id,
            data,
        )
    except Exception as e:
        handle_error(e)


# order routes

@router.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
)
def create_order(data: OrderCreate):
    try:
        return OrderService.create_order(data)
    except Exception as e:
        handle_error(e)


@router.get("/orders/number/{order_number}")
def get_order_by_number(order_number: str):
    try:
        return OrderService.get_order_by_number(order_number)
    except Exception as e:
        handle_error(e)


@router.get("/orders")
def get_orders():
    try:
        return OrderService.get_orders()
    except Exception as e:
        handle_error(e)


@router.get("/orders/{order_id}")
def get_order(order_id: str):
    try:
        return OrderService.get_order(order_id)
    except Exception as e:
        handle_error(e)


@router.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: str,
    data: OrderStatusUpdate,
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
):
    try:
        return OrderService.update_discount(
            order_id,
            data.discount,
        )
    except Exception as e:
        handle_error(e)


# order item routes

@router.post(
    "/orders/{order_id}/items",
    status_code=status.HTTP_201_CREATED,
)
def add_order_item(
    order_id: str,
    data: OrderItemCreate,
):
    try:
        return OrderItemService.add_item(
            order_id,
            data,
        )
    except Exception as e:
        handle_error(e)


@router.get("/orders/{order_id}/items")
def get_order_items(order_id: str):
    try:
        return OrderItemService.get_order_items(order_id)
    except Exception as e:
        handle_error(e)


@router.put("/orders/{order_id}/items/{item_id}")
def update_order_item(
    order_id: str,
    item_id: str,
    data: OrderItemUpdate,
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
):
    try:
        return OrderItemService.delete_item(
            order_id,
            item_id,
        )
    except Exception as e:
        handle_error(e)


@router.post("/orders/{order_id}/recalculate")
def recalculate_order(order_id: str):
    try:
        return OrderItemService.recalculate_order(order_id)
    except Exception as e:
        handle_error(e)


# kitchen routes

@router.post(
    "/kitchen/tickets",
    status_code=status.HTTP_201_CREATED,
)
def create_kitchen_ticket(data: KitchenTicketCreate):
    try:
        return KitchenService.create_ticket(
            data.order_id,
            data.priority,
        )
    except Exception as e:
        handle_error(e)


@router.get("/kitchen/tickets/{ticket_id}")
def get_kitchen_ticket(ticket_id: str):
    try:
        return KitchenService.get_ticket(ticket_id)
    except Exception as e:
        handle_error(e)


@router.patch("/kitchen/tickets/{ticket_id}/status")
def update_kitchen_ticket_status(
    ticket_id: str,
    data: dict,
):
    try:
        if "status" not in data:
            raise ValueError("status is required")

        return KitchenService.update_ticket_status(
            ticket_id,
            data["status"],
        )
    except Exception as e:
        handle_error(e)


@router.post(
    "/kitchen/tickets/{ticket_id}/assign",
    status_code=status.HTTP_201_CREATED,
)
def assign_kitchen_staff(
    ticket_id: str,
    data: KitchenStaffAssignment,
):
    try:
        return KitchenService.assign_staff(
            ticket_id,
            data.staff_id,
        )
    except Exception as e:
        handle_error(e)


# stock movement routes

@router.post(
    "/stock-movements",
    status_code=status.HTTP_201_CREATED,
)
def create_stock_movement(data: dict):
    try:
        return StockMovementService.create_movement(data)
    except Exception as e:
        handle_error(e)


@router.get("/stock-movements")
def get_stock_movements():
    try:
        return StockMovementService.get_movements()
    except Exception as e:
        handle_error(e)


@router.get("/stock-movements/ingredient/{ingredient_id}")
def get_ingredient_stock_movements(ingredient_id: str):
    try:
        return StockMovementService.get_by_ingredient(
            ingredient_id
        )
    except Exception as e:
        handle_error(e)


# billing routes

@router.post(
    "/invoices",
    status_code=status.HTTP_201_CREATED,
)
def create_invoice(data: InvoiceCreate):
    try:
        return BillingService.create_invoice(data.order_id)
    except Exception as e:
        handle_error(e)


@router.get("/invoices/order/{order_id}")
def get_order_invoice(order_id: str):
    try:
        return BillingService.get_invoice_by_order(order_id)
    except Exception as e:
        handle_error(e)


@router.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: str):
    try:
        return BillingService.get_invoice(invoice_id)
    except Exception as e:
        handle_error(e)


# payment routes

@router.post(
    "/payments",
    status_code=status.HTTP_201_CREATED,
)
def create_payment(data: PaymentCreate):
    try:
        return PaymentService.create_payment(data)
    except Exception as e:
        handle_error(e)


@router.get("/payments/invoice/{invoice_id}")
def get_invoice_payments(invoice_id: str):
    try:
        return PaymentService.get_invoice_payments(invoice_id)
    except Exception as e:
        handle_error(e)


@router.get("/payments/{payment_id}")
def get_payment(payment_id: str):
    try:
        return PaymentService.get_payment(payment_id)
    except Exception as e:
        handle_error(e)


# refund routes

@router.post(
    "/refunds",
    status_code=status.HTTP_201_CREATED,
)
def create_refund(data: RefundCreate):
    try:
        return RefundService.create_refund(data)
    except Exception as e:
        handle_error(e)


@router.patch("/refunds/{refund_id}/approve")
def approve_refund(
    refund_id: str,
    data: RefundApproval,
):
    try:
        return RefundService.approve_refund(
            refund_id,
            data,
        )
    except Exception as e:
        handle_error(e)


@router.get("/refunds/order/{order_id}")
def get_order_refunds(order_id: str):
    try:
        return RefundService.get_order_refunds(order_id)
    except Exception as e:
        handle_error(e)


@router.get("/refunds/{refund_id}")
def get_refund(refund_id: str):
    try:
        return RefundService.get_refund(refund_id)
    except Exception as e:
        handle_error(e)


# activity log routes

@router.post(
    "/orders/{order_id}/activity",
    status_code=status.HTTP_201_CREATED,
)
def create_activity_log(
    order_id: str,
    data: dict,
):
    try:
        if not data.get("action"):
            raise ValueError("action is required")

        return ActivityLogService.create_log(
            order_id=order_id,
            action=data["action"],
            performed_by=data.get("performed_by"),
            details=data.get("details"),
        )
    except Exception as e:
        handle_error(e)


@router.get("/orders/{order_id}/activity")
def get_order_activity(order_id: str):
    try:
        return ActivityLogService.get_order_logs(order_id)
    except Exception as e:
        handle_error(e)


# kitchen event routes

@router.post(
    "/kitchen/events",
    status_code=status.HTTP_201_CREATED,
)
def create_kitchen_event(data: dict):
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
def get_order_kitchen_events(order_id: str):
    try:
        return KitchenEventService.get_order_events(order_id)
    except Exception as e:
        handle_error(e)


# feedback routes

@router.post(
    "/orders/{order_id}/feedback",
    status_code=status.HTTP_201_CREATED,
)
def create_feedback(
    order_id: str,
    data: FeedbackCreate,
):
    try:
        return FeedbackService.create_feedback(
            order_id,
            data,
        )
    except Exception as e:
        handle_error(e)


@router.get("/feedback/{feedback_id}")
def get_feedback(feedback_id: str):
    try:
        return FeedbackService.get_feedback(feedback_id)
    except Exception as e:
        handle_error(e)


@router.get("/feedback/customer/{customer_id}")
def get_customer_feedback(customer_id: str):
    try:
        return FeedbackService.get_customer_feedback(
            customer_id
        )
    except Exception as e:
        handle_error(e)


@router.get("/feedback/order/{order_id}")
def get_order_feedback(order_id: str):
    try:
        return FeedbackService.get_order_feedback(order_id)
    except Exception as e:
        handle_error(e)


@router.get("/feedback/summary")
def get_feedback_summary():
    try:
        return FeedbackService.get_summary()
    except Exception as e:
        handle_error(e)


@router.get("/feedback")
def get_all_feedback():
    try:
        return FeedbackService.get_all_feedback()
    except Exception as e:
        handle_error(e)
=======
"""
Master router bridge module.
Re-exports the combined APIRouter from modular route modules in app/routes/.
Maintains 100% backward compatibility for all imports from app.routes.routes.
"""

from app.routes import (
    router,
    handle_error,
    get_current_user,
    require_roles,
    security,
    auth_router,
    user_router,
    customer_router,
    menu_router,
    ingredient_router,
    recipe_router,
    table_router,
    reservation_router,
    order_router,
    kitchen_router,
    stock_movement_router,
    payment_router,
    activity_log_router,
    kitchen_event_router,
    feedback_router,
)

__all__ = [
    "router",
    "handle_error",
    "get_current_user",
    "require_roles",
    "security",
    "auth_router",
    "user_router",
    "customer_router",
    "menu_router",
    "ingredient_router",
    "recipe_router",
    "table_router",
    "reservation_router",
    "order_router",
    "kitchen_router",
    "stock_movement_router",
    "payment_router",
    "activity_log_router",
    "kitchen_event_router",
    "feedback_router",
]
>>>>>>> main
