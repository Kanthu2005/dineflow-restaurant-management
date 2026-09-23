
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.config.settings import settings


print(settings.MONGO_URL)
print(settings.DATABASE_NAME)


app = FastAPI(title="Restaurant API")


# ============================================================
# TEMPORARY DATA
# ============================================================

users_data = [
    {
        "id": 1,
        "name": "Akhil",
        "email": "akhil@example.com"
    }
]

customers_data = [
    {
        "id": 1,
        "name": "Rahul",
        "phone": "9876543210"
    }
]

menu_data = [
    {
        "id": 1,
        "name": "Chicken Biryani",
        "price": 250
    },
    {
        "id": 2,
        "name": "Paneer Biryani",
        "price": 200
    }
]

orders_data = [
    {
        "id": 1,
        "customer_id": 1,
        "item": "Chicken Biryani",
        "quantity": 2,
        "status": "Pending"
    }
]


# ============================================================
# PYDANTIC SCHEMAS
# ============================================================

class UserCreate(BaseModel):
    name: str
    email: str


class CustomerCreate(BaseModel):
    name: str
    phone: str


class MenuCreate(BaseModel):
    name: str
    price: float


class OrderCreate(BaseModel):
    customer_id: int
    item: str
    quantity: int
    status: str = "Pending"


class UserUpdate(BaseModel):
    name: str
    email: str


class CustomerUpdate(BaseModel):
    name: str
    phone: str


class MenuUpdate(BaseModel):
    name: str
    price: float


class OrderUpdate(BaseModel):
    customer_id: int
    item: str
    quantity: int
    status: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Restaurant API is running"
    }


# ============================================================
# USERS
# ============================================================

# GET - Get all users
@app.get("/users")
def get_users():
    return users_data


# GET - Get one user
@app.get("/users/{user_id}")
def get_user(user_id: int):

    for user in users_data:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# POST - Create user
@app.post("/users", status_code=201)
def create_user(user: UserCreate):

    new_user = {
        "id": len(users_data) + 1,
        "name": user.name,
        "email": user.email
    }

    users_data.append(new_user)

    return new_user


# PUT - Update complete user
@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):

    for existing_user in users_data:

        if existing_user["id"] == user_id:

            existing_user["name"] = user.name
            existing_user["email"] = user.email

            return existing_user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# PATCH - Partial update user
@app.patch("/users/{user_id}")
def patch_user(user_id: int, user: UserCreate):

    for existing_user in users_data:

        if existing_user["id"] == user_id:

            existing_user["name"] = user.name
            existing_user["email"] = user.email

            return existing_user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# DELETE - Delete user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    for user in users_data:

        if user["id"] == user_id:

            users_data.remove(user)

            return {
                "message": "User deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# ============================================================
# CUSTOMERS
# ============================================================

# GET
@app.get("/customers")
def get_customers():
    return customers_data


# GET by ID
@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):

    for customer in customers_data:

        if customer["id"] == customer_id:
            return customer

    raise HTTPException(
        status_code=404,
        detail="Customer not found"
    )


# POST
@app.post("/customers", status_code=201)
def create_customer(customer: CustomerCreate):

    new_customer = {
        "id": len(customers_data) + 1,
        "name": customer.name,
        "phone": customer.phone
    }

    customers_data.append(new_customer)

    return new_customer


# PUT
@app.put("/customers/{customer_id}")
def update_customer(
    customer_id: int,
    customer: CustomerUpdate
):

    for existing_customer in customers_data:

        if existing_customer["id"] == customer_id:

            existing_customer["name"] = customer.name
            existing_customer["phone"] = customer.phone

            return existing_customer

    raise HTTPException(
        status_code=404,
        detail="Customer not found"
    )


# DELETE
@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):

    for customer in customers_data:

        if customer["id"] == customer_id:

            customers_data.remove(customer)

            return {
                "message": "Customer deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Customer not found"
    )


# ============================================================
# MENU
# ============================================================

# GET
@app.get("/menu")
def get_menu():
    return menu_data


# GET by ID
@app.get("/menu/{menu_id}")
def get_menu_item(menu_id: int):

    for item in menu_data:

        if item["id"] == menu_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Menu item not found"
    )


# POST
@app.post("/menu", status_code=201)
def create_menu_item(item: MenuCreate):

    new_item = {
        "id": len(menu_data) + 1,
        "name": item.name,
        "price": item.price
    }

    menu_data.append(new_item)

    return new_item


# PUT
@app.put("/menu/{menu_id}")
def update_menu_item(
    menu_id: int,
    item: MenuUpdate
):

    for existing_item in menu_data:

        if existing_item["id"] == menu_id:

            existing_item["name"] = item.name
            existing_item["price"] = item.price

            return existing_item

    raise HTTPException(
        status_code=404,
        detail="Menu item not found"
    )


# DELETE
@app.delete("/menu/{menu_id}")
def delete_menu_item(menu_id: int):

    for item in menu_data:

        if item["id"] == menu_id:

            menu_data.remove(item)

            return {
                "message": "Menu item deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Menu item not found"
    )


# ============================================================
# ORDERS
# ============================================================

# GET
@app.get("/orders")
def get_orders():
    return orders_data


# GET by ID
@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for order in orders_data:

        if order["id"] == order_id:
            return order

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )


# POST
@app.post("/orders", status_code=201)
def create_order(order: OrderCreate):

    new_order = {
        "id": len(orders_data) + 1,
        "customer_id": order.customer_id,
        "item": order.item,
        "quantity": order.quantity,
        "status": order.status
    }

    orders_data.append(new_order)

    return new_order


# PUT
@app.put("/orders/{order_id}")
def update_order(
    order_id: int,
    order: OrderUpdate
):

    for existing_order in orders_data:

        if existing_order["id"] == order_id:

            existing_order["customer_id"] = order.customer_id
            existing_order["item"] = order.item
            existing_order["quantity"] = order.quantity
            existing_order["status"] = order.status

            return existing_order

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )


# PATCH
@app.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str
):

    for order in orders_data:

        if order["id"] == order_id:

            order["status"] = status

            return order

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )


# DELETE
@app.delete("/orders/{order_id}")
def delete_order(order_id: int):

    for order in orders_data:

        if order["id"] == order_id:

            orders_data.remove(order)

            return {
                "message": "Order deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=settings.PORT,
        reload=True
    )

