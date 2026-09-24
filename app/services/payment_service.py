from decimal import Decimal
from bson import ObjectId
from bson.decimal128 import Decimal128
from app.database.mongodb import (
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
            "paid_at": now_utc(),
            "recorded_by": data.recorded_by,
        }
        if getattr(data, "transaction_reference", None):
            payment["transaction_reference"] = data.transaction_reference

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

    @staticmethod
    def get_by_invoice(invoice_id):
        return PaymentService.get_invoice_payments(invoice_id)


#refundservice...
