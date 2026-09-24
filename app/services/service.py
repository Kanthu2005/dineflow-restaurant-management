from datetime import datetime, timezone
from decimal import Decimal
from bson import ObjectId
from bson.decimal128 import Decimal128

from app.database.mongodb import (
    users_collection,
    customers_collection,
    menu_categories_collection,
    menu_items_collection,
    ingredients_collection,
    recipes_collection,
    restaurant_tables_collection,
    reservations_collection,
    orders_collection,
    order_items_collection,
    kitchen_tickets_collection,
    kitchen_ticket_items_collection,
    staff_assignments_collection,
    stock_movements_collection,
    invoices_collection,
    payments_collection,
    refunds_collection,
    order_activity_logs_collection,
    kitchen_events_collection,
    customer_feedback_collection,
)


#commonhelpers...
def now_utc():
    return datetime.now(timezone.utc)


def to_object_id(value: str):
    if not ObjectId.is_valid(value):
        raise ValueError("Invalid ID")
    return ObjectId(value)


def decimal128(value):
    if isinstance(value, Decimal128):
        return value
    return Decimal128(Decimal(str(value)))


def convert_decimal(value):
    if isinstance(value, Decimal128):
        return value.to_decimal()

    if isinstance(value, dict):
        return {
            key: convert_decimal(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            convert_decimal(item)
            for item in value
        ]

    return value


def serialize_document(document):
    if not document:
        return None

    document = document.copy()

    if "_id" in document:
        document["id"] = str(document.pop("_id"))

    return convert_decimal(document)


def serialize_documents(documents):
    return [
        serialize_document(document)
        for document in documents
    ]


def generate_number(prefix: str):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}-{timestamp}"


#userservice...
class UserService:

    @staticmethod
    def create_user(data):

        if users_collection.find_one(
            {"email": data.email.lower()}
        ):
            raise ValueError("Email already exists")

        user = {
            "name": data.name,
            "email": data.email.lower(),
            "password": data.password,
            "role": data.role,
            "is_active": True,
            "created_at": now_utc(),
        }

        result = users_collection.insert_one(user)

        user["_id"] = result.inserted_id

        return serialize_document(user)

    @staticmethod
    def get_user(user_id):

        user = users_collection.find_one(
            {"_id": to_object_id(user_id)}
        )

        if not user:
            raise ValueError("User not found")

        return serialize_document(user)

    @staticmethod
    def get_users():

        users = users_collection.find().sort(
            "created_at",
            -1
        )

        return serialize_documents(users)

    @staticmethod
    def update_user(user_id, data):

        update_data = data.model_dump(
            exclude_unset=True
        )

        if not update_data:
            raise ValueError("No data to update")

        if "email" in update_data:
            update_data["email"] = update_data["email"].lower()

        result = users_collection.update_one(
            {"_id": to_object_id(user_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise ValueError("User not found")

        return UserService.get_user(user_id)

    @staticmethod
    def delete_user(user_id):

        result = users_collection.delete_one(
            {"_id": to_object_id(user_id)}
        )

        if result.deleted_count == 0:
            raise ValueError("User not found")

        return {"message": "User deleted successfully"}


#customerservice...
class CustomerService:

    @staticmethod
    def create_customer(data):

        if customers_collection.find_one(
            {"phone": data.phone}
        ):
            raise ValueError("Phone number already exists")

        customer = {
            "name": data.name,
            "phone": data.phone,
            "email": (
                data.email.lower()
                if data.email
                else None
            ),
            "created_at": now_utc(),
        }

        result = customers_collection.insert_one(customer)

        customer["_id"] = result.inserted_id

        return serialize_document(customer)

    @staticmethod
    def get_customer(customer_id):

        customer = customers_collection.find_one(
            {"_id": to_object_id(customer_id)}
        )

        if not customer:
            raise ValueError("Customer not found")

        return serialize_document(customer)

    @staticmethod
    def get_customers():

        customers = customers_collection.find().sort(
            "created_at",
            -1
        )

        return serialize_documents(customers)

    @staticmethod
    def update_customer(customer_id, data):

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "email" in update_data and update_data["email"]:
            update_data["email"] = update_data["email"].lower()

        result = customers_collection.update_one(
            {"_id": to_object_id(customer_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise ValueError("Customer not found")

        return CustomerService.get_customer(customer_id)



#menucategoryservice...
class MenuCategoryService:

    @staticmethod
    def create_category(data):

        if menu_categories_collection.find_one(
            {"name": data.name}
        ):
            raise ValueError("Category already exists")

        category = {
            "name": data.name,
            "description": data.description,
            "created_at": now_utc(),
        }

        result = menu_categories_collection.insert_one(category)

        category["_id"] = result.inserted_id

        return serialize_document(category)

    @staticmethod
    def get_categories():

        categories = menu_categories_collection.find().sort(
            "name",
            1
        )

        return serialize_documents(categories)

    @staticmethod
    def get_category(category_id):

        category = menu_categories_collection.find_one(
            {"_id": to_object_id(category_id)}
        )

        if not category:
            raise ValueError("Category not found")

        return serialize_document(category)

    @staticmethod
    def update_category(category_id, data):

        update_data = data.model_dump(
            exclude_unset=True
        )

        result = menu_categories_collection.update_one(
            {"_id": to_object_id(category_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise ValueError("Category not found")

        return MenuCategoryService.get_category(category_id)



#menuitemservice...
class MenuItemService:

    @staticmethod
    def create_item(data):

        category = menu_categories_collection.find_one(
            {"_id": to_object_id(data.category_id)}
        )

        if not category:
            raise ValueError("Category not found")

        item = {
            "name": data.name,
            "description": data.description,
            "category_id": to_object_id(data.category_id),
            "price": decimal128(data.price),
            "preparation_time": data.preparation_time,
            "is_available": data.is_available,
            "is_vegetarian": data.is_vegetarian,
            "created_at": now_utc(),
        }

        result = menu_items_collection.insert_one(item)

        item["_id"] = result.inserted_id

        return serialize_document(item)

    @staticmethod
    def get_items():

        items = menu_items_collection.find().sort(
            "name",
            1
        )

        return serialize_documents(items)

    @staticmethod
    def get_item(item_id):

        item = menu_items_collection.find_one(
            {"_id": to_object_id(item_id)}
        )

        if not item:
            raise ValueError("Menu item not found")

        return serialize_document(item)

    @staticmethod
    def get_available_items():

        items = menu_items_collection.find(
            {"is_available": True}
        )

        return serialize_documents(items)

    @staticmethod
    def get_items_by_category(category_id):

        items = menu_items_collection.find(
            {
                "category_id": to_object_id(category_id)
            }
        )

        return serialize_documents(items)

    @staticmethod
    def update_item(item_id, data):

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "category_id" in update_data:
            update_data["category_id"] = to_object_id(
                update_data["category_id"]
            )

        if "price" in update_data:
            update_data["price"] = decimal128(
                update_data["price"]
            )

        result = menu_items_collection.update_one(
            {"_id": to_object_id(item_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise ValueError("Menu item not found")

        return MenuItemService.get_item(item_id)



#ingredientservice...
class IngredientService:

    @staticmethod
    def create_ingredient(data):

        if ingredients_collection.find_one(
            {"name": data.name}
        ):
            raise ValueError("Ingredient already exists")

        ingredient = {
            "name": data.name,
            "unit": data.unit,
            "available_quantity": decimal128(
                data.available_quantity
            ),
            "minimum_stock_level": decimal128(
                data.minimum_stock_level
            ),
            "cost_per_unit": decimal128(
                data.cost_per_unit
            ),
            "supplier_name": data.supplier_name,
            "is_active": data.is_active,
            "created_at": now_utc(),
        }

        result = ingredients_collection.insert_one(
            ingredient
        )

        ingredient["_id"] = result.inserted_id

        return serialize_document(ingredient)

    @staticmethod
    def get_ingredients():

        ingredients = ingredients_collection.find().sort(
            "name",
            1
        )

        return serialize_documents(ingredients)

    @staticmethod
    def get_active_ingredients():

        ingredients = ingredients_collection.find(
            {"is_active": True}
        )

        return serialize_documents(ingredients)

    @staticmethod
    def get_ingredient(ingredient_id):

        ingredient = ingredients_collection.find_one(
            {"_id": to_object_id(ingredient_id)}
        )

        if not ingredient:
            raise ValueError("Ingredient not found")

        return serialize_document(ingredient)

    @staticmethod
    def update_ingredient(ingredient_id, data):

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field in [
            "minimum_stock_level",
            "cost_per_unit",
        ]:
            if field in update_data:
                update_data[field] = decimal128(
                    update_data[field]
                )

        result = ingredients_collection.update_one(
            {"_id": to_object_id(ingredient_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise ValueError("Ingredient not found")

        return IngredientService.get_ingredient(
            ingredient_id
        )

    @staticmethod
    def update_stock(ingredient_id, quantity):

        result = ingredients_collection.update_one(
            {"_id": to_object_id(ingredient_id)},
            {
                "$inc": {
                    "available_quantity": decimal128(
                        quantity
                    )
                }
            }
        )

        if result.matched_count == 0:
            raise ValueError("Ingredient not found")

        return IngredientService.get_ingredient(
            ingredient_id
        )

    @staticmethod
    def get_stock_status(ingredient_id):

        ingredient = IngredientService.get_ingredient(
            ingredient_id
        )

        available = ingredient["available_quantity"]
        minimum = ingredient["minimum_stock_level"]

        if available <= 0:
            status = "OUT_OF_STOCK"
        elif available <= minimum:
            status = "CRITICAL"
        elif available <= minimum * Decimal("1.5"):
            status = "LOW"
        else:
            status = "NORMAL"

        return {
            "ingredient_id": ingredient_id,
            "ingredient_name": ingredient["name"],
            "available_quantity": available,
            "minimum_stock_level": minimum,
            "status": status,
        }



#recipeservice...
class RecipeService:

    @staticmethod
    def create_recipe(menu_item_id, data):

        menu_item = menu_items_collection.find_one(
            {"_id": to_object_id(menu_item_id)}
        )

        if not menu_item:
            raise ValueError("Menu item not found")

        ingredient = ingredients_collection.find_one(
            {"_id": to_object_id(data.ingredient_id)}
        )

        if not ingredient:
            raise ValueError("Ingredient not found")

        existing = recipes_collection.find_one(
            {
                "menu_item_id": to_object_id(menu_item_id),
                "ingredient_id": to_object_id(
                    data.ingredient_id
                ),
            }
        )

        if existing:
            raise ValueError(
                "Ingredient already exists in recipe"
            )

        recipe = {
            "menu_item_id": to_object_id(menu_item_id),
            "ingredient_id": to_object_id(
                data.ingredient_id
            ),
            "quantity_required": decimal128(
                data.quantity_required
            ),
        }

        result = recipes_collection.insert_one(recipe)

        recipe["_id"] = result.inserted_id

        return serialize_document(recipe)

    @staticmethod
    def get_recipe(menu_item_id):

        recipes = recipes_collection.find(
            {
                "menu_item_id": to_object_id(
                    menu_item_id
                )
            }
        )

        return serialize_documents(recipes)

    @staticmethod
    def get_recipe_by_id(recipe_id):

        recipe = recipes_collection.find_one(
            {"_id": to_object_id(recipe_id)}
        )

        if not recipe:
            raise ValueError("Recipe not found")

        return serialize_document(recipe)

    @staticmethod
    def update_recipe(recipe_id, data):

        result = recipes_collection.update_one(
            {"_id": to_object_id(recipe_id)},
            {
                "$set": {
                    "quantity_required": decimal128(
                        data.quantity_required
                    )
                }
            }
        )

        if result.matched_count == 0:
            raise ValueError("Recipe not found")

        return RecipeService.get_recipe_by_id(recipe_id)


# ============================================================
# 7. TABLE SERVICE
# ============================================================

class RestaurantTableService:

    @staticmethod
    def create_table(data):

        if restaurant_tables_collection.find_one(
            {"table_number": data.table_number}
        ):
            raise ValueError("Table number already exists")

        table = {
            "table_number": data.table_number,
            "capacity": data.capacity,
            "location": data.location,
            "status": "AVAILABLE",
            "is_active": data.is_active,
        }

        result = restaurant_tables_collection.insert_one(table)

        table["_id"] = result.inserted_id

        return serialize_document(table)

    @staticmethod
    def get_tables():

        tables = restaurant_tables_collection.find().sort(
            "table_number",
            1
        )

        return serialize_documents(tables)

    @staticmethod
    def get_table(table_id):

        table = restaurant_tables_collection.find_one(
            {"_id": to_object_id(table_id)}
        )

        if not table:
            raise ValueError("Table not found")

        return serialize_document(table)

    @staticmethod
    def get_available_tables():

        tables = restaurant_tables_collection.find(
            {
                "status": "AVAILABLE",
                "is_active": True,
            }
        )

        return serialize_documents(tables)

    @staticmethod
    def update_table(table_id, data):

        update_data = data.model_dump(
            exclude_unset=True
        )

        result = restaurant_tables_collection.update_one(
            {"_id": to_object_id(table_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise ValueError("Table not found")

        return RestaurantTableService.get_table(table_id)

    @staticmethod
    def update_status(table_id, status):

        result = restaurant_tables_collection.update_one(
            {"_id": to_object_id(table_id)},
            {"$set": {"status": status}}
        )

        if result.matched_count == 0:
            raise ValueError("Table not found")

        return RestaurantTableService.get_table(table_id)



#reservationservice...
class ReservationService:

    @staticmethod
    def create_reservation(data):

        customer = customers_collection.find_one(
            {"_id": to_object_id(data.customer_id)}
        )

        if not customer:
            raise ValueError("Customer not found")

        table = restaurant_tables_collection.find_one(
            {"_id": to_object_id(data.table_id)}
        )

        if not table:
            raise ValueError("Table not found")

        if not table["is_active"]:
            raise ValueError("Table is inactive")

        if data.guest_count > table["capacity"]:
            raise ValueError(
                "Guest count exceeds table capacity"
            )

        existing = reservations_collection.find_one(
            {
                "table_id": to_object_id(data.table_id),
                "reservation_date": data.reservation_date,
                "status": {
                    "$in": [
                        "REQUESTED",
                        "CONFIRMED",
                        "SEATED",
                    ]
                },
                "$expr": {
                    "$and": [
                        {
                            "$lt": [
                                "$start_time",
                                data.end_time,
                            ]
                        },
                        {
                            "$gt": [
                                "$end_time",
                                data.start_time,
                            ]
                        },
                    ]
                },
            }
        )

        if existing:
            raise ValueError(
                "Table already reserved for this time"
            )

        reservation = {
            "customer_id": to_object_id(
                data.customer_id
            ),
            "table_id": to_object_id(
                data.table_id
            ),
            "reservation_date": data.reservation_date,
            "start_time": data.start_time,
            "end_time": data.end_time,
            "guest_count": data.guest_count,
            "status": "REQUESTED",
            "contact_number": data.contact_number,
            "created_at": now_utc(),
        }

        result = reservations_collection.insert_one(
            reservation
        )

        reservation["_id"] = result.inserted_id

        return serialize_document(reservation)

    @staticmethod
    def get_reservations():

        reservations = reservations_collection.find().sort(
            "created_at",
            -1
        )

        return serialize_documents(reservations)

    @staticmethod
    def get_reservation(reservation_id):

        reservation = reservations_collection.find_one(
            {"_id": to_object_id(reservation_id)}
        )

        if not reservation:
            raise ValueError("Reservation not found")

        return serialize_document(reservation)

    @staticmethod
    def get_by_customer(customer_id):

        reservations = reservations_collection.find(
            {
                "customer_id": to_object_id(
                    customer_id
                )
            }
        )

        return serialize_documents(reservations)

    @staticmethod
    def get_by_table(table_id):

        reservations = reservations_collection.find(
            {
                "table_id": to_object_id(table_id)
            }
        )

        return serialize_documents(reservations)


#orderservice...
class OrderService:

    @staticmethod
    def create_order(data):

        if data.customer_id:

            customer = customers_collection.find_one(
                {"_id": to_object_id(data.customer_id)}
            )

            if not customer:
                raise ValueError("Customer not found")

        if data.table_id:

            table = restaurant_tables_collection.find_one(
                {"_id": to_object_id(data.table_id)}
            )

            if not table:
                raise ValueError("Table not found")

            if table["status"] == "OCCUPIED":
                raise ValueError(
                    "Table is already occupied"
                )

        order = {
            "order_number": generate_number("ORD"),
            "customer_id": (
                to_object_id(data.customer_id)
                if data.customer_id
                else None
            ),
            "table_id": (
                to_object_id(data.table_id)
                if data.table_id
                else None
            ),
            "order_type": data.order_type,
            "status": "DRAFT",
            "subtotal": Decimal128("0"),
            "tax_amount": Decimal128("0"),
            "discount_amount": Decimal128("0"),
            "total_amount": Decimal128("0"),
            "created_by": data.created_by,
            "created_at": now_utc(),
        }

        result = orders_collection.insert_one(order)

        order["_id"] = result.inserted_id

        return serialize_document(order)

    @staticmethod
    def get_orders():

        orders = orders_collection.find().sort(
            "created_at",
            -1
        )

        return serialize_documents(orders)

    @staticmethod
    def get_order(order_id):

        order = orders_collection.find_one(
            {"_id": to_object_id(order_id)}
        )

        if not order:
            raise ValueError("Order not found")

        return serialize_document(order)

    @staticmethod
    def get_order_by_number(order_number):

        order = orders_collection.find_one(
            {"order_number": order_number}
        )

        if not order:
            raise ValueError("Order not found")

        return serialize_document(order)

    @staticmethod
    def update_status(order_id, status):

        order = orders_collection.find_one(
            {"_id": to_object_id(order_id)}
        )

        if not order:
            raise ValueError("Order not found")

        result = orders_collection.update_one(
            {"_id": order["_id"]},
            {"$set": {"status": status}}
        )

        return OrderService.get_order(order_id)


#orderitemservice...
class OrderItemService:

    @staticmethod
    def add_item(order_id, data):

        order = orders_collection.find_one(
            {"_id": to_object_id(order_id)}
        )

        if not order:
            raise ValueError("Order not found")

        if order["status"] != "DRAFT":
            raise ValueError(
                "Items can only be added to draft orders"
            )

        menu_item = menu_items_collection.find_one(
            {"_id": to_object_id(data.menu_item_id)}
        )

        if not menu_item:
            raise ValueError("Menu item not found")

        if not menu_item["is_available"]:
            raise ValueError(
                "Menu item is not available"
            )

        unit_price = menu_item["price"]

        item_total = unit_price * data.quantity

        item = {
            "order_id": order["_id"],
            "menu_item_id": menu_item["_id"],
            "item_name_snapshot": menu_item["name"],
            "unit_price_snapshot": unit_price,
            "quantity": data.quantity,
            "special_instructions": (
                data.special_instructions
            ),
            "item_total": item_total,
        }

        result = order_items_collection.insert_one(item)

        item["_id"] = result.inserted_id

        OrderItemService.recalculate_order(order_id)

        return serialize_document(item)

    @staticmethod
    def get_order_items(order_id):

        items = order_items_collection.find(
            {
                "order_id": to_object_id(order_id)
            }
        )

        return serialize_documents(items)

    @staticmethod
    def recalculate_order(order_id):

        items = list(
            order_items_collection.find(
                {
                    "order_id": to_object_id(order_id)
                }
            )
        )

        subtotal = Decimal("0")

        for item in items:
            subtotal += (
                item["unit_price_snapshot"]
                .to_decimal()
                * item["quantity"]
            )

        tax = subtotal * Decimal("0.05")

        order = orders_collection.find_one(
            {"_id": to_object_id(order_id)}
        )

        discount = (
            order["discount_amount"]
            .to_decimal()
            if order
            else Decimal("0")
        )

        total = subtotal + tax - discount

        if total < 0:
            total = Decimal("0")

        orders_collection.update_one(
            {"_id": to_object_id(order_id)},
            {
                "$set": {
                    "subtotal": decimal128(subtotal),
                    "tax_amount": decimal128(tax),
                    "total_amount": decimal128(total),
                }
            }
        )

        return OrderService.get_order(order_id)



#kitchenservice...
class KitchenService:

    @staticmethod
    def create_ticket(order_id, priority="NORMAL"):

        order = orders_collection.find_one(
            {"_id": to_object_id(order_id)}
        )

        if not order:
            raise ValueError("Order not found")

        if order["status"] != "CONFIRMED":
            raise ValueError(
                "Only confirmed orders can go to kitchen"
            )

        existing = kitchen_tickets_collection.find_one(
            {"order_id": order["_id"]}
        )

        if existing:
            raise ValueError(
                "Kitchen ticket already exists"
            )

        ticket = {
            "order_id": order["_id"],
            "status": "QUEUED",
            "priority": priority,
            "assigned_staff_id": None,
            "started_at": None,
            "ready_at": None,
            "completed_at": None,
        }

        result = kitchen_tickets_collection.insert_one(
            ticket
        )

        ticket["_id"] = result.inserted_id

        orders_collection.update_one(
            {"_id": order["_id"]},
            {"$set": {"status": "SENT_TO_KITCHEN"}}
        )

        return serialize_document(ticket)

    @staticmethod
    def get_ticket(ticket_id):

        ticket = kitchen_tickets_collection.find_one(
            {"_id": to_object_id(ticket_id)}
        )

        if not ticket:
            raise ValueError("Kitchen ticket not found")

        return serialize_document(ticket)

    @staticmethod
    def update_ticket_status(ticket_id, status):

        ticket = kitchen_tickets_collection.find_one(
            {"_id": to_object_id(ticket_id)}
        )

        if not ticket:
            raise ValueError("Kitchen ticket not found")

        update_data = {
            "status": status
        }

        if status == "PREPARING":
            update_data["started_at"] = now_utc()

        elif status == "READY":
            update_data["ready_at"] = now_utc()

        elif status == "HANDED_OVER":
            update_data["completed_at"] = now_utc()

        kitchen_tickets_collection.update_one(
            {"_id": ticket["_id"]},
            {"$set": update_data}
        )

        return KitchenService.get_ticket(ticket_id)

    @staticmethod
    def assign_staff(ticket_id, staff_id):

        ticket = kitchen_tickets_collection.find_one(
            {"_id": to_object_id(ticket_id)}
        )

        if not ticket:
            raise ValueError("Kitchen ticket not found")

        assignment = {
            "kitchen_ticket_id": ticket["_id"],
            "staff_id": staff_id,
            "assigned_at": now_utc(),
            "unassigned_at": None,
        }

        result = staff_assignments_collection.insert_one(
            assignment
        )

        staff_assignments_collection.update_many(
            {
                "kitchen_ticket_id": ticket["_id"],
                "staff_id": {
                    "$ne": staff_id
                },
                "unassigned_at": None,
            },
            {
                "$set": {
                    "unassigned_at": now_utc()
                }
            }
        )

        kitchen_tickets_collection.update_one(
            {"_id": ticket["_id"]},
            {
                "$set": {
                    "assigned_staff_id": staff_id
                }
            }
        )

        assignment["_id"] = result.inserted_id

        return serialize_document(assignment)



#stockmovementservice...
class StockMovementService:

    @staticmethod
    def create_movement(data):

        ingredient = ingredients_collection.find_one(
            {"_id": to_object_id(data.ingredient_id)}
        )

        if not ingredient:
            raise ValueError("Ingredient not found")

        quantity = Decimal(str(data.quantity))

        if data.movement_type in [
            "OUT",
            "USAGE",
            "WASTE",
        ]:

            available = ingredient[
                "available_quantity"
            ].to_decimal()

            if quantity > available:
                raise ValueError(
                    "Insufficient stock"
                )

            quantity_change = -quantity

        else:
            quantity_change = quantity

        ingredients_collection.update_one(
            {"_id": ingredient["_id"]},
            {
                "$inc": {
                    "available_quantity": decimal128(
                        quantity_change
                    )
                }
            }
        )

        movement = {
            "ingredient_id": ingredient["_id"],
            "movement_type": data.movement_type,
            "quantity": decimal128(quantity),
            "reference_type": data.reference_type,
            "reference_id": data.reference_id,
            "created_by": data.created_by,
            "created_at": now_utc(),
        }

        result = stock_movements_collection.insert_one(
            movement
        )

        movement["_id"] = result.inserted_id

        return serialize_document(movement)

    @staticmethod
    def get_movements():

        movements = stock_movements_collection.find().sort(
            "created_at",
            -1
        )

        return serialize_documents(movements)

    @staticmethod
    def get_by_ingredient(ingredient_id):

        movements = stock_movements_collection.find(
            {
                "ingredient_id": to_object_id(
                    ingredient_id
                )
            }
        ).sort(
            "created_at",
            -1
        )

        return serialize_documents(movements)


#billingservice...

class BillingService:

    @staticmethod
    def create_invoice(order_id):

        order = orders_collection.find_one(
            {"_id": to_object_id(order_id)}
        )

        if not order:
            raise ValueError("Order not found")

        existing = invoices_collection.find_one(
            {"order_id": order["_id"]}
        )

        if existing:
            raise ValueError(
                "Invoice already exists"
            )

        invoice = {
            "order_id": order["_id"],
            "invoice_number": generate_number("INV"),
            "subtotal": order["subtotal"],
            "discount_amount": order[
                "discount_amount"
            ],
            "tax_amount": order["tax_amount"],
            "total_amount": order["total_amount"],
            "status": "UNPAID",
            "generated_at": now_utc(),
        }

        result = invoices_collection.insert_one(
            invoice
        )

        invoice["_id"] = result.inserted_id

        return serialize_document(invoice)

    @staticmethod
    def get_invoice(invoice_id):

        invoice = invoices_collection.find_one(
            {"_id": to_object_id(invoice_id)}
        )

        if not invoice:
            raise ValueError("Invoice not found")

        return serialize_document(invoice)

    @staticmethod
    def get_invoice_by_order(order_id):

        invoice = invoices_collection.find_one(
            {"order_id": to_object_id(order_id)}
        )

        if not invoice:
            raise ValueError("Invoice not found")

        return serialize_document(invoice)



#paymentservice...
class PaymentService:

    @staticmethod
    def create_payment(data):

        invoice = invoices_collection.find_one(
            {"_id": to_object_id(data.invoice_id)}
        )

        if not invoice:
            raise ValueError("Invoice not found")

        amount = Decimal(str(data.amount))

        existing_payments = payments_collection.find(
            {
                "invoice_id": invoice["_id"],
                "payment_status": "SUCCESS",
            }
        )

        paid_amount = Decimal("0")

        for payment in existing_payments:
            paid_amount += payment["amount"].to_decimal()

        outstanding = (
            invoice["total_amount"].to_decimal()
            - paid_amount
        )

        if amount > outstanding:
            raise ValueError(
                "Payment exceeds outstanding amount"
            )

        if data.transaction_reference:

            duplicate = payments_collection.find_one(
                {
                    "transaction_reference":
                        data.transaction_reference
                }
            )

            if duplicate:
                raise ValueError(
                    "Transaction reference already exists"
                )

        payment = {
            "invoice_id": invoice["_id"],
            "amount": decimal128(amount),
            "payment_method": data.payment_method,
            "payment_status": "SUCCESS",
            "transaction_reference":
                data.transaction_reference,
            "paid_at": now_utc(),
            "recorded_by": data.recorded_by,
        }

        result = payments_collection.insert_one(
            payment
        )

        payment["_id"] = result.inserted_id

        new_paid_amount = paid_amount + amount

        if new_paid_amount >= invoice[
            "total_amount"
        ].to_decimal():

            invoices_collection.update_one(
                {"_id": invoice["_id"]},
                {"$set": {"status": "PAID"}}
            )

            orders_collection.update_one(
                {"_id": invoice["order_id"]},
                {"$set": {"status": "COMPLETED"}}
            )

        else:

            invoices_collection.update_one(
                {"_id": invoice["_id"]},
                {"$set": {"status": "PARTIALLY_PAID"}}
            )

        return serialize_document(payment)

    @staticmethod
    def get_payment(payment_id):

        payment = payments_collection.find_one(
            {"_id": to_object_id(payment_id)}
        )

        if not payment:
            raise ValueError("Payment not found")

        return serialize_document(payment)

    @staticmethod
    def get_invoice_payments(invoice_id):

        payments = payments_collection.find(
            {
                "invoice_id": to_object_id(
                    invoice_id
                )
            }
        ).sort(
            "paid_at",
            -1
        )

        return serialize_documents(payments)


#refundservice...
class RefundService:

    @staticmethod
    def create_refund(data):

        payment = payments_collection.find_one(
            {"_id": to_object_id(data.payment_id)}
        )

        if not payment:
            raise ValueError("Payment not found")

        refund = {
            "payment_id": payment["_id"],
            "order_id": to_object_id(data.order_id),
            "requested_amount": decimal128(
                data.requested_amount
            ),
            "approved_amount": decimal128("0"),
            "reason": data.reason,
            "status": "REQUESTED",
            "approved_by": None,
            "processed_at": None,
            "created_at": now_utc(),
        }

        result = refunds_collection.insert_one(refund)

        refund["_id"] = result.inserted_id

        return serialize_document(refund)

    @staticmethod
    def approve_refund(refund_id, data):

        refund = refunds_collection.find_one(
            {"_id": to_object_id(refund_id)}
        )

        if not refund:
            raise ValueError("Refund not found")

        requested = refund[
            "requested_amount"
        ].to_decimal()

        approved = Decimal(
            str(data.approved_amount)
        )

        if approved > requested:
            raise ValueError(
                "Approved amount cannot exceed requested amount"
            )

        refunds_collection.update_one(
            {"_id": refund["_id"]},
            {
                "$set": {
                    "approved_amount":
                        decimal128(approved),
                    "approved_by":
                        data.approved_by,
                    "status": "APPROVED",
                }
            }
        )

        return RefundService.get_refund(refund_id)

    @staticmethod
    def get_refund(refund_id):

        refund = refunds_collection.find_one(
            {"_id": to_object_id(refund_id)}
        )

        if not refund:
            raise ValueError("Refund not found")

        return serialize_document(refund)

    @staticmethod
    def get_order_refunds(order_id):

        refunds = refunds_collection.find(
            {
                "order_id": to_object_id(order_id)
            }
        )

        return serialize_documents(refunds)



#activitylogservice...
class ActivityLogService:

    @staticmethod
    def create_log(
        order_id,
        action,
        performed_by=None,
        details=None,
    ):

        log = {
            "order_id": to_object_id(order_id),
            "action": action,
            "performed_by": performed_by,
            "details": details,
            "created_at": now_utc(),
        }

        result = order_activity_logs_collection.insert_one(
            log
        )

        log["_id"] = result.inserted_id

        return serialize_document(log)

    @staticmethod
    def get_order_logs(order_id):

        logs = order_activity_logs_collection.find(
            {
                "order_id": to_object_id(order_id)
            }
        ).sort(
            "created_at",
            -1
        )

        return serialize_documents(logs)


#kitcheneventservice
class KitchenEventService:

    @staticmethod
    def create_event(
        order_id,
        event_type,
        kitchen_ticket_id=None,
        details=None,
    ):

        event = {
            "order_id": to_object_id(order_id),
            "kitchen_ticket_id": (
                to_object_id(kitchen_ticket_id)
                if kitchen_ticket_id
                else None
            ),
            "event_type": event_type,
            "details": details,
            "created_at": now_utc(),
        }

        result = kitchen_events_collection.insert_one(
            event
        )

        event["_id"] = result.inserted_id

        return serialize_document(event)

    @staticmethod
    def get_order_events(order_id):

        events = kitchen_events_collection.find(
            {
                "order_id": to_object_id(order_id)
            }
        ).sort(
            "created_at",
            -1
        )

        return serialize_documents(events)



#feedbackservice...
class FeedbackService:

    @staticmethod
    def create_feedback(order_id, data):

        order = orders_collection.find_one(
            {"_id": to_object_id(order_id)}
        )

        if not order:
            raise ValueError("Order not found")

        existing = customer_feedback_collection.find_one(
            {
                "order_id": order["_id"],
                "customer_id": to_object_id(
                    data.customer_id
                ),
            }
        )

        if existing:
            raise ValueError(
                "Feedback already submitted for this order"
            )

        feedback = {
            "order_id": order["_id"],
            "customer_id": to_object_id(
                data.customer_id
            ),
            "rating": data.rating,
            "food_rating": data.food_rating,
            "service_rating": data.service_rating,
            "comments": data.comments,
            "created_at": now_utc(),
        }

        result = customer_feedback_collection.insert_one(
            feedback
        )

        feedback["_id"] = result.inserted_id

        return serialize_document(feedback)

    @staticmethod
    def get_feedback(feedback_id):

        feedback = customer_feedback_collection.find_one(
            {"_id": to_object_id(feedback_id)}
        )

        if not feedback:
            raise ValueError("Feedback not found")

        return serialize_document(feedback)

    @staticmethod
    def get_customer_feedback(customer_id):

        feedback = customer_feedback_collection.find(
            {
                "customer_id": to_object_id(
                    customer_id
                )
            }
        ).sort(
            "created_at",
            -1
        )

        return serialize_documents(feedback)

    @staticmethod
    def get_order_feedback(order_id):

        feedback = customer_feedback_collection.find(
            {
                "order_id": to_object_id(order_id)
            }
        )

        return serialize_documents(feedback)

    @staticmethod
    def get_all_feedback():

        feedback = customer_feedback_collection.find().sort(
            "created_at",
            -1
        )

        return serialize_documents(feedback)

    @staticmethod
    def get_summary():

        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_feedback": {
                        "$sum": 1
                    },
                    "average_rating": {
                        "$avg": "$rating"
                    },
                    "average_food_rating": {
                        "$avg": "$food_rating"
                    },
                    "average_service_rating": {
                        "$avg": "$service_rating"
                    },
                }
            }
        ]

        result = list(
            customer_feedback_collection.aggregate(
                pipeline
            )
        )

        if not result:
            return {
                "total_feedback": 0,
                "average_rating": 0,
                "average_food_rating": 0,
                "average_service_rating": 0,
            }

        summary = result[0]

        return {
            "total_feedback":
                summary["total_feedback"],
            "average_rating":
                round(summary["average_rating"], 2),
            "average_food_rating":
                round(
                    summary["average_food_rating"],
                    2
                ),
            "average_service_rating":
                round(
                    summary["average_service_rating"],
                    2
                ),
        }