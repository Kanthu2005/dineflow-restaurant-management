from fastapi import APIRouter, HTTPException

from schemas.table_schema import (
    RestaurantTableCreate,
    RestaurantTableUpdate,
    TableStatusUpdate
)

from services.table_service import RestaurantTableService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/tables")
def create_table(table: RestaurantTableCreate):
    try:
        return RestaurantTableService.create_table(table)
    except Exception as error:
        handle_error(error)


@router.get("/tables/available")
def get_available_tables():
    try:
        return RestaurantTableService.get_available_tables()
    except Exception as error:
        handle_error(error)


@router.get("/tables")
def get_tables():
    try:
        return RestaurantTableService.get_tables()
    except Exception as error:
        handle_error(error)


@router.get("/tables/{table_id}")
def get_table(table_id: int):
    try:
        return RestaurantTableService.get_table(table_id)
    except Exception as error:
        handle_error(error)


@router.put("/tables/{table_id}")
def update_table(
    table_id: int,
    table: RestaurantTableUpdate
):
    try:
        return RestaurantTableService.update_table(
            table_id,
            table
        )
    except Exception as error:
        handle_error(error)


@router.patch("/tables/{table_id}/status")
def update_table_status(
    table_id: int,
    status: TableStatusUpdate
):
    try:
        return RestaurantTableService.update_table_status(
            table_id,
            status
        )
    except Exception as error:
        handle_error(error)