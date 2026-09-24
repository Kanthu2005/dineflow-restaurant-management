from decimal import Decimal
from bson import ObjectId
from bson.decimal128 import Decimal128
from app.database.mongodb import (
    refunds_collection,
    payments_collection,
    invoices_collection,
    orders_collection,
)
from app.services.common import (
    now_utc,
    to_object_id,
    decimal128,
    generate_number,
    serialize_document,
    serialize_documents,
)


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

    @staticmethod
    def get_by_order(order_id):
        return RefundService.get_order_refunds(order_id)



#activitylogservice...
