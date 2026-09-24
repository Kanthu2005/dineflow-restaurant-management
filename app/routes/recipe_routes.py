from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.recipe_schema import RecipeCreate, RecipeUpdate
from app.services.recipe_service import RecipeService
from app.routes.dependencies import handle_error, get_current_user, require_roles

router = APIRouter(tags=["Recipes"])


@router.post(
    "/recipes",
    status_code=status.HTTP_201_CREATED,
)
def create_recipe(
    data: RecipeCreate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF")),
):
    try:
        return RecipeService.create_recipe(data)
    except Exception as e:
        handle_error(e)


@router.get("/menu/items/{menu_item_id}/recipes")
def get_recipes_by_menu_item(
    menu_item_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF")),
):
    try:
        return RecipeService.get_by_menu_item(
            menu_item_id
        )
    except Exception as e:
        handle_error(e)


@router.get("/recipes/{recipe_id}")
def get_recipe(
    recipe_id: str,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF")),
):
    try:
        return RecipeService.get_recipe(recipe_id)
    except Exception as e:
        handle_error(e)


@router.put("/recipes/{recipe_id}")
def update_recipe(
    recipe_id: str,
    data: RecipeUpdate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF")),
):
    try:
        return RecipeService.update_recipe(
            recipe_id,
            data,
        )
    except Exception as e:
        handle_error(e)
