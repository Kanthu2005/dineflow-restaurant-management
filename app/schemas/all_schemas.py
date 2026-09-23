from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ============================================================
# 1. USER SCHEMAS
# ============================================================

class UserCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=6)
    role: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    is_active: bool = True


# ============================================================
# 2. CUSTOMER SCHEMAS
# ============================================================

class CustomerCreate(BaseModel):
    name: str = Field(min_length=2)
    phone: str
    email: EmailStr | None = None


class CustomerResponse(BaseModel):
    id: str
    name: str
    phone: str
    email: EmailStr | None = None


# ============================================================
# 3. MENU SCHEMAS
# ============================================================

class MenuCategoryCreate(BaseModel):
    name: str = Field(min_length=2)
    description: str = ""


class MenuCategoryResponse(BaseModel):
    id: str
    name: str
    description: str


class MenuItemCreate(BaseModel):
    name: str = Field(min_length=2)
    description: str = ""
    category_id: str
    price: float = Field(gt=0)
    preparation_time: int = Field(gt=0)
    is_available: bool = True
    is_vegetarian: bool = False


class MenuItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category_id: str | None = None
    price: float | None = Field(default=None, gt=0)
    preparation_time: int | None = Field(default=None, gt=0)
    is_available: bool | None = None
    is_vegetarian: bool | None = None


class MenuItemResponse(BaseModel):
    id: str
    name: str
    description: str
    category_id: str
    price: float
    preparation_time: int
    is_available: bool
    is_vegetarian: bool


# ============================================================
# 4. INGREDIENT SCHEMAS
# ============================================================

class IngredientCreate(BaseModel):
    name: str = Field(min_length=2)
    unit: str
    current_stock: float = Field(ge=0)
    minimum_stock: float = Field(ge=0)


class IngredientUpdate(BaseModel):
    name: str | None = None
    unit: str | None = None
    current_stock: float | None = Field(default=None, ge=0)
    minimum_stock: float | None = Field(default=None, ge=0)


class IngredientResponse(BaseModel):
    id: str
    name: str
    unit: str
    current_stock: float
    minimum_stock: float


# ============================================================
# 5. RECIPE SCHEMAS
# ============================================================

class RecipeIngredient(BaseModel):
    ingredient_id: str
    quantity: float = Field(gt=0)


class RecipeCreate(BaseModel):
    menu_item_id: str
    ingredients: list[RecipeIngredient]


class RecipeResponse(BaseModel):
    id: str
    menu_item_id: str
    ingredients: list[RecipeIngredient]


# ============================================================
# 6. RESTAURANT TABLE SCHEMAS
# ============================================================

class RestaurantTableCreate(BaseModel):
    table_number: int = Field(gt=0)
    capacity: int = Field(gt=0)
    status: str = "available"


class RestaurantTableUpdate(BaseModel):
    capacity: int | None = Field(default=None, gt=0)
    status: str | None = None


class RestaurantTableResponse(BaseModel):
    id: str
    table_number: int
    capacity: int
    status: str


# ============================================================
# 7. RESERVATION SCHEMAS
# ============================================================

class ReservationCreate(BaseModel):
    customer_id: str
    table_id: str
    reservation_time: datetime
    number_of_guests: int = Field(gt=0)


class ReservationUpdate(BaseModel):
    reservation_time: datetime | None = None
    number_of_guests: int | None = Field(default=None, gt=0)
    status: str | None = None


class ReservationResponse(BaseModel):
    id: str
    customer_id: str
    table_id: str
    reservation_time: datetime
    number_of_guests: int
    status: str


# ============================================================
# 8. ORDER SCHEMAS
# ============================================================

class OrderItemCreate(BaseModel):
    menu_item_id: str
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_id: str | None = None
    table_id: str | None = None
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemResponse(BaseModel):
    menu_item_id: str
    quantity: int
    unit_price: float
    subtotal: float


class OrderResponse(BaseModel):
    id: str
    customer_id: str | None
    table_id: str | None
    items: list[OrderItemResponse]
    total_amount: float
    status: str


# ============================================================
# 9. KITCHEN SCHEMAS
# ============================================================

class KitchenTicketItem(BaseModel):
    menu_item_id: str
    quantity: int = Field(gt=0)


class KitchenTicketCreate(BaseModel):
    order_id: str
    items: list[KitchenTicketItem]


class KitchenTicketUpdate(BaseModel):
    status: str


class KitchenTicketResponse(BaseModel):
    id: str
    order_id: str
    items: list[KitchenTicketItem]
    status: str
    assigned_staff_id: str | None = None


# ============================================================
# 10. STAFF ASSIGNMENT SCHEMAS
# ============================================================

class StaffAssignmentCreate(BaseModel):
    kitchen_ticket_id: str
    staff_id: str


class StaffAssignmentResponse(BaseModel):
    id: str
    kitchen_ticket_id: str
    staff_id: str
    status: str


# ============================================================
# 11. INVENTORY / STOCK MOVEMENT SCHEMAS
# ============================================================

class StockMovementCreate(BaseModel):
    ingredient_id: str
    quantity: float = Field(gt=0)
    movement_type: str
    reason: str


class StockMovementResponse(BaseModel):
    id: str
    ingredient_id: str
    quantity: float
    movement_type: str
    reason: str


# ============================================================
# 12. BILLING / INVOICE SCHEMAS
# ============================================================

class InvoiceCreate(BaseModel):
    order_id: str
    subtotal: float = Field(ge=0)
    tax: float = Field(ge=0)
    discount: float = Field(ge=0, default=0)


class InvoiceResponse(BaseModel):
    id: str
    order_id: str
    subtotal: float
    tax: float
    discount: float
    total_amount: float
    status: str


# ============================================================
# 13. PAYMENT SCHEMAS
# ============================================================

class PaymentCreate(BaseModel):
    invoice_id: str
    amount: float = Field(gt=0)
    payment_method: str


class PaymentResponse(BaseModel):
    id: str
    invoice_id: str
    amount: float
    payment_method: str
    status: str


# ============================================================
# 14. REFUND SCHEMAS
# ============================================================

class RefundCreate(BaseModel):
    payment_id: str
    amount: float = Field(gt=0)
    reason: str


class RefundResponse(BaseModel):
    id: str
    payment_id: str
    amount: float
    reason: str
    status: str


# ============================================================
# 15. CUSTOMER FEEDBACK SCHEMAS
# ============================================================

class FeedbackCreate(BaseModel):
    customer_id: str
    order_id: str
    rating: int = Field(ge=1, le=5)
    comment: str = ""


class FeedbackResponse(BaseModel):
    id: str
    customer_id: str
    order_id: str
    rating: int
    comment: str