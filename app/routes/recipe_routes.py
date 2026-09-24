from fastapi import APIRouter, HTTPException

from schemas.recipe_schema import RecipeCreate, RecipeUpdate
from services.recipe_service import RecipeService

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


@router.post("/menu/items/{menu_item_id}/recipes")
def create_recipe(
    menu_item_id: int,
    recipe: RecipeCreate
):
    try:
        return RecipeService.create_recipe(
            menu_item_id,
            recipe
        )
    except Exception as error:
        handle_error(error)


@router.get("/menu/items/{menu_item_id}/recipes")
def get_recipes(menu_item_id: int):
    try:
        return RecipeService.get_recipes(menu_item_id)
    except Exception as error:
        handle_error(error)


@router.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int):
    try:
        return RecipeService.get_recipe(recipe_id)
    except Exception as error:
        handle_error(error)


@router.put("/recipes/{recipe_id}")
def update_recipe(
    recipe_id: int,
    recipe: RecipeUpdate
):
    try:
        return RecipeService.update_recipe(
            recipe_id,
            recipe
        )
    except Exception as error:
        handle_error(error)