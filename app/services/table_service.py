from bson import ObjectId
from app.database.mongodb import restaurant_tables_collection
from app.services.common import (
    now_utc,
    to_object_id,
    serialize_document,
    serialize_documents,
)


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
