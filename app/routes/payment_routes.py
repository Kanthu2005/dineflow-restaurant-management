from fastapi import APIRouter, HTTPException

from schemas.payment_schema import PaymentCreate
from services.payment_service import PaymentService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/payments")
def create_payment(payment: PaymentCreate):
    try:
        return PaymentService.create_payment(payment)
    except Exception as error:
        handle_error(error)


@router.get("/payments/invoice/{invoice_id}")
def get_invoice_payments(invoice_id: int):
    try:
        return PaymentService.get_invoice_payments(invoice_id)
    except Exception as error:
        handle_error(error)


@router.get("/payments/{payment_id}")
def get_payment(payment_id: int):
    try:
        return PaymentService.get_payment(payment_id)
    except Exception as error:
        handle_error(error)