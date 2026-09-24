from decimal import Decimal
from bson import ObjectId
from bson.decimal128 import Decimal128
from app.database.mongodb import (
    orders_collection,
    order_items_collection,
    menu_items_collection,
    restaurant_tables_collection,
    customers_collection,
)
from app.services.common import (
    now_utc,
    to_object_id,
    decimal128,
    generate_number,
    serialize_document,
    serialize_documents,
)


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

    @staticmethod
    def update_discount(order_id, data):
        order = orders_collection.find_one(
            {"_id": to_object_id(order_id)}
        )
        if not order:
            raise ValueError("Order not found")

        discount_val = getattr(data, "discount_amount", data)
        discount = Decimal(str(discount_val))
        if discount < 0:
            raise ValueError("Discount amount cannot be negative")

        orders_collection.update_one(
            {"_id": order["_id"]},
            {"$set": {"discount_amount": decimal128(discount)}}
        )
        return OrderItemService.recalculate_order(order_id)


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
        unit_price_dec = unit_price.to_decimal() if isinstance(unit_price, Decimal128) else Decimal(str(unit_price))
        item_total = decimal128(unit_price_dec * Decimal(str(data.quantity)))

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
    def update_item(order_id, item_id, data):
        order = orders_collection.find_one(
            {"_id": to_object_id(order_id)}
        )
        if not order:
            raise ValueError("Order not found")
        if order["status"] != "DRAFT":
            raise ValueError("Items can only be updated in draft orders")

        item = order_items_collection.find_one(
            {
                "_id": to_object_id(item_id),
                "order_id": order["_id"],
            }
        )
        if not item:
            raise ValueError("Order item not found")

        update_data = {}
        if getattr(data, "quantity", None) is not None:
            unit_price = item["unit_price_snapshot"]
            unit_price_dec = unit_price.to_decimal() if isinstance(unit_price, Decimal128) else Decimal(str(unit_price))
            update_data["quantity"] = data.quantity
            update_data["item_total"] = decimal128(unit_price_dec * Decimal(str(data.quantity)))

        if getattr(data, "special_instructions", None) is not None:
            update_data["special_instructions"] = data.special_instructions

        if update_data:
            order_items_collection.update_one(
                {"_id": item["_id"]},
                {"$set": update_data}
            )
            OrderItemService.recalculate_order(order_id)

        updated = order_items_collection.find_one({"_id": item["_id"]})
        return serialize_document(updated)

    @staticmethod
    def delete_item(order_id, item_id):
        order = orders_collection.find_one(
            {"_id": to_object_id(order_id)}
        )
        if not order:
            raise ValueError("Order not found")
        if order["status"] != "DRAFT":
            raise ValueError("Items can only be deleted from draft orders")

        result = order_items_collection.delete_one(
            {
                "_id": to_object_id(item_id),
                "order_id": order["_id"],
            }
        )
        if result.deleted_count == 0:
            raise ValueError("Order item not found")

        OrderItemService.recalculate_order(order_id)
        return {"message": "Order item deleted successfully"}

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
