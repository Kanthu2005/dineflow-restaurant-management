from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.menu_schema import (
    MenuCategoryCreate,
    MenuCategoryUpdate,
    MenuItemCreate,
    MenuItemUpdate,
)
from app.services.menu_service import MenuCategoryService, MenuItemService
from app.routes.dependencies import handle_error, get_current_user, require_roles

router = APIRouter(tags=["Menu"])


@router.post(
    "/menu/categories",
    status_code=status.HTTP_201_CREATED,
)
def create_menu_category(
    data: MenuCategoryCreate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF")),
):
    try:
        return MenuCategoryService.create_category(data)
    except Exception as e:
        handle_error(e)


@router.get("/menu/categories")
def get_menu_categories(current_user: dict = Depends(get_current_user)):
    try:
        return MenuCategoryService.get_categories()
    except Exception as e:
        handle_error(e)


@router.get("/menu/categories/{category_id}")
def get_menu_category(
    category_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        return MenuCategoryService.get_category(category_id)
    except Exception as e:
        handle_error(e)


@router.put("/menu/categories/{category_id}")
def update_menu_category(
    category_id: str,
    data: MenuCategoryUpdate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF")),
):
    try:
        return MenuCategoryService.update_category(
            category_id,
            data,
        )
    except Exception as e:
        handle_error(e)


# ==========================================
# Menu Item Routes
# ==========================================

@router.post(
    "/menu/items",
    status_code=status.HTTP_201_CREATED,
)
def create_menu_item(
    data: MenuItemCreate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF")),
):
    try:
        return MenuItemService.create_item(data)
    except Exception as e:
        handle_error(e)


@router.get("/menu/items/available")
def get_available_menu_items(current_user: dict = Depends(get_current_user)):
    try:
        return MenuItemService.get_available_items()
    except Exception as e:
        handle_error(e)


@router.get("/menu/items/category/{category_id}")
def get_menu_items_by_category(
    category_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        return MenuItemService.get_items_by_category(category_id)
    except Exception as e:
        handle_error(e)


@router.get("/menu/items")
def get_menu_items(current_user: dict = Depends(get_current_user)):
    try:
        return MenuItemService.get_items()
    except Exception as e:
        handle_error(e)


@router.get("/menu/items/{item_id}")
def get_menu_item(
    item_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        return MenuItemService.get_item(item_id)
    except Exception as e:
        handle_error(e)


@router.put("/menu/items/{item_id}")
def update_menu_item(
    item_id: str,
    data: MenuItemUpdate,
    current_user: dict = Depends(require_roles("ADMIN", "MANAGER", "CHEF")),
):
    try:
        return MenuItemService.update_item(
            item_id,
            data,
        )
    except Exception as e:
        handle_error(e)
