from fastapi import APIRouter, HTTPException

from schemas.stock_schema import StockMovementCreate
from services.stock_movement_service import StockMovementService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/stock-movements")
def create_stock_movement(movement: StockMovementCreate):
    try:
        return StockMovementService.create_movement(movement)
    except Exception as error:
        handle_error(error)


@router.get("/stock-movements")
def get_stock_movements():
    try:
        return StockMovementService.get_movements()
    except Exception as error:
        handle_error(error)


@router.get("/stock-movements/ingredient/{ingredient_id}")
def get_ingredient_movements(ingredient_id: int):
    try:
        return StockMovementService.get_ingredient_movements(
            ingredient_id
        )
    except Exception as error:
        handle_error(error)