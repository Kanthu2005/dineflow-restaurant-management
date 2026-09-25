from decimal import Decimal
from bson import ObjectId
from bson.decimal128 import Decimal128
from app.database.mongodb import (
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

    @staticmethod
    def get_by_order(order_id):
        return BillingService.get_invoice_by_order(order_id)

    @staticmethod
    def get_invoices(status=None):
        query = {}
        if status:
            query["status"] = status
        invoices = list(invoices_collection.find(query).sort("_id", -1))
        enriched = []
        for inv in invoices:
            item = serialize_document(inv)
            if "order_id" in inv and inv["order_id"]:
                order = orders_collection.find_one({"_id": inv["order_id"]})
                if order:
                    item["order_number"] = order.get("order_number")
                    item["order_type"] = order.get("order_type")
            enriched.append(item)
        return enriched



#paymentservice...
