from bson import ObjectId
from app.database.mongodb import order_activity_logs_collection
from app.services.common import (
    now_utc,
    to_object_id,
    serialize_document,
    serialize_documents,
)


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
