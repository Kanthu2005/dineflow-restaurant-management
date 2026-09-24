from fastapi import APIRouter, HTTPException

from schemas.reservation_schema import (
    ReservationCreate,
    ReservationUpdate
)

from services.reservation_service import ReservationService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/reservations")
def create_reservation(reservation: ReservationCreate):
    try:
        return ReservationService.create_reservation(reservation)
    except Exception as error:
        handle_error(error)


@router.get("/reservations")
def get_reservations():
    try:
        return ReservationService.get_reservations()
    except Exception as error:
        handle_error(error)


@router.get("/reservations/customer/{customer_id}")
def get_customer_reservations(customer_id: int):
    try:
        return ReservationService.get_customer_reservations(customer_id)
    except Exception as error:
        handle_error(error)


@router.get("/reservations/table/{table_id}")
def get_table_reservations(table_id: int):
    try:
        return ReservationService.get_table_reservations(table_id)
    except Exception as error:
        handle_error(error)


@router.get("/reservations/{reservation_id}")
def get_reservation(reservation_id: int):
    try:
        return ReservationService.get_reservation(reservation_id)
    except Exception as error:
        handle_error(error)


@router.put("/reservations/{reservation_id}")
def update_reservation(
    reservation_id: int,
    reservation: ReservationUpdate
):
    try:
        return ReservationService.update_reservation(
            reservation_id,
            reservation
        )
    except Exception as error:
        handle_error(error)