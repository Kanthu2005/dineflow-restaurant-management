from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.payments_schema import (
    InvoiceCreate,
    PaymentCreate,
    RefundCreate,
    RefundApproval,
)
from app.services.billing_service import BillingService
from app.services.payment_service import PaymentService
from app.services.refund_service import RefundService
from app.routes.dependencies import handle_error, get_current_user, require_roles

router = APIRouter(tags=["Billing & Payments"])


@router.post(
    "/invoices",
    status_code=status.HTTP_201_CREATED,
)
def create_invoice(
    data: InvoiceCreate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CASHIER")),
):
    try:
        return BillingService.create_invoice(
            data.order_id
        )
    except Exception as e:
        handle_error(e)


@router.get("/invoices/order/{order_id}")
def get_order_invoice(
    order_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CASHIER")),
):
    try:
        return BillingService.get_by_order(order_id)
    except Exception as e:
        handle_error(e)


@router.get("/invoices/{invoice_id}")
def get_invoice(
    invoice_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CASHIER")),
):
    try:
        return BillingService.get_invoice(invoice_id)
    except Exception as e:
        handle_error(e)


# ==========================================
# Payment Routes
# ==========================================

@router.post(
    "/payments",
    status_code=status.HTTP_201_CREATED,
)
def create_payment(
    data: PaymentCreate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CASHIER")),
):
    try:
        return PaymentService.create_payment(data)
    except Exception as e:
        handle_error(e)


@router.get("/payments/invoice/{invoice_id}")
def get_invoice_payments(
    invoice_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CASHIER")),
):
    try:
        return PaymentService.get_by_invoice(
            invoice_id
        )
    except Exception as e:
        handle_error(e)


@router.get("/payments/{payment_id}")
def get_payment(
    payment_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CASHIER")),
):
    try:
        return PaymentService.get_payment(payment_id)
    except Exception as e:
        handle_error(e)


# ==========================================
# Refund Routes
# ==========================================

@router.post(
    "/refunds",
    status_code=status.HTTP_201_CREATED,
)
def create_refund(
    data: RefundCreate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CASHIER")),
):
    try:
        return RefundService.create_refund(data)
    except Exception as e:
        handle_error(e)


@router.patch("/refunds/{refund_id}/approve")
def approve_refund(
    refund_id: str,
    data: RefundApproval,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER")),
):
    try:
        return RefundService.approve_refund(
            refund_id,
            data,
        )
    except Exception as e:
        handle_error(e)


@router.get("/refunds/order/{order_id}")
def get_order_refunds(
    order_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CASHIER")),
):
    try:
        return RefundService.get_by_order(order_id)
    except Exception as e:
        handle_error(e)


@router.get("/refunds/{refund_id}")
def get_refund(
    refund_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CASHIER")),
):
    try:
        return RefundService.get_refund(refund_id)
    except Exception as e:
        handle_error(e)
