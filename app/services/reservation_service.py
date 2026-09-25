from bson import ObjectId
from app.database.mongodb import (
    reservations_collection,
    restaurant_tables_collection,
    customers_collection,
)
from app.services.common import (
    now_utc,
    to_object_id,
    serialize_document,
    serialize_documents,
)


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

        res_date_str = str(data.reservation_date)
        start_time_str = str(data.start_time)
        end_time_str = str(data.end_time)

        existing = reservations_collection.find_one(
            {
                "table_id": to_object_id(data.table_id),
                "reservation_date": res_date_str,
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
                                end_time_str,
                            ]
                        },
                        {
                            "$gt": [
                                "$end_time",
                                start_time_str,
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
            "reservation_date": res_date_str,
            "start_time": start_time_str,
            "end_time": end_time_str,
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

    @staticmethod
    def update_reservation(reservation_id, data):
        reservation = reservations_collection.find_one(
            {"_id": to_object_id(reservation_id)}
        )
        if not reservation:
            raise ValueError("Reservation not found")

        update_data = data.model_dump(exclude_unset=True) if hasattr(data, "model_dump") else data.copy()
        if not update_data:
            raise ValueError("No data to update")

        if "table_id" in update_data and update_data["table_id"]:
            update_data["table_id"] = to_object_id(update_data["table_id"])
        if "customer_id" in update_data and update_data["customer_id"]:
            update_data["customer_id"] = to_object_id(update_data["customer_id"])
        for dt_field in ["reservation_date", "start_time", "end_time"]:
            if dt_field in update_data and update_data[dt_field] is not None:
                update_data[dt_field] = str(update_data[dt_field])

        update_data["updated_at"] = now_utc()
        reservations_collection.update_one(
            {"_id": reservation["_id"]},
            {"$set": update_data}
        )
        return ReservationService.get_reservation(reservation_id)


#orderservice...
