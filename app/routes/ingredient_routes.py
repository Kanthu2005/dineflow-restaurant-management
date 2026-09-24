from fastapi import APIRouter, HTTPException

from schemas.ingredient_schema import (
    IngredientCreate,
    IngredientUpdate,
    StockUpdate
)

from services.ingredient_service import IngredientService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/ingredients")
def create_ingredient(ingredient: IngredientCreate):
    try:
        return IngredientService.create_ingredient(ingredient)
    except Exception as error:
        handle_error(error)


@router.get("/ingredients/active")
def get_active_ingredients():
    try:
        return IngredientService.get_active_ingredients()
    except Exception as error:
        handle_error(error)


@router.get("/ingredients")
def get_ingredients():
    try:
        return IngredientService.get_ingredients()
    except Exception as error:
        handle_error(error)


@router.get("/ingredients/{ingredient_id}")
def get_ingredient(ingredient_id: int):
    try:
        return IngredientService.get_ingredient(ingredient_id)
    except Exception as error:
        handle_error(error)


@router.put("/ingredients/{ingredient_id}")
def update_ingredient(
    ingredient_id: int,
    ingredient: IngredientUpdate
):
    try:
        return IngredientService.update_ingredient(
            ingredient_id,
            ingredient
        )
    except Exception as error:
        handle_error(error)


@router.post("/ingredients/{ingredient_id}/stock")
def update_stock(
    ingredient_id: int,
    stock: StockUpdate
):
    try:
        return IngredientService.update_stock(
            ingredient_id,
            stock
        )
    except Exception as error:
        handle_error(error)


@router.get("/ingredients/{ingredient_id}/stock-status")
def get_stock_status(ingredient_id: int):
    try:
        return IngredientService.get_stock_status(ingredient_id)
    except Exception as error:
        handle_error(error)