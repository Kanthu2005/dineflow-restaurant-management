from fastapi import APIRouter, HTTPException

from schemas.billing_schema import InvoiceCreate
from services.billing_service import BillingService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/invoices")
def create_invoice(invoice: InvoiceCreate):
    try:
        return BillingService.create_invoice(invoice)
    except Exception as error:
        handle_error(error)


@router.get("/invoices/order/{order_id}")
def get_order_invoice(order_id: int):
    try:
        return BillingService.get_order_invoice(order_id)
    except Exception as error:
        handle_error(error)


@router.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int):
    try:
        return BillingService.get_invoice(invoice_id)
    except Exception as error:
        handle_error(error)