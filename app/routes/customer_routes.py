from fastapi import APIRouter, HTTPException

from schemas.customer_schema import CustomerCreate, CustomerUpdate
from services.customer_service import CustomerService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/customers")
def create_customer(customer: CustomerCreate):
    try:
        return CustomerService.create_customer(customer)
    except Exception as error:
        handle_error(error)


@router.get("/customers")
def get_customers():
    try:
        return CustomerService.get_customers()
    except Exception as error:
        handle_error(error)


@router.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    try:
        return CustomerService.get_customer(customer_id)
    except Exception as error:
        handle_error(error)


@router.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: CustomerUpdate):
    try:
        return CustomerService.update_customer(customer_id, customer)
    except Exception as error:
        handle_error(error)