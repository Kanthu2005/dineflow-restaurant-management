from bson import ObjectId
from app.database.mongodb import (
    kitchen_tickets_collection,
    kitchen_ticket_items_collection,
    staff_assignments_collection,
    orders_collection,
    order_items_collection,
    users_collection,
)
from app.services.common import (
    now_utc,
    to_object_id,
    generate_number,
    serialize_document,
    serialize_documents,
)


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
