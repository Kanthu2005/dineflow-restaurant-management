from fastapi import APIRouter, HTTPException

from schemas.menu_schema import (
    MenuCategoryCreate,
    MenuCategoryUpdate,
    MenuItemCreate,
    MenuItemUpdate
)

from services.menu_service import (
    MenuCategoryService,
    MenuItemService
)

router = APIRouter()


def handle_error(error):
    raise HTTPException(status_code=400, detail=str(error))


# ---------------- MENU CATEGORIES ----------------

@router.post("/menu/categories")
def create_category(category: MenuCategoryCreate):
    try:
        return MenuCategoryService.create_category(category)
    except Exception as error:
        handle_error(error)


@router.get("/menu/categories")
def get_categories():
    try:
        return MenuCategoryService.get_categories()
    except Exception as error:
        handle_error(error)


@router.get("/menu/categories/{category_id}")
def get_category(category_id: int):
    try:
        return MenuCategoryService.get_category(category_id)
    except Exception as error:
        handle_error(error)


@router.put("/menu/categories/{category_id}")
def update_category(
    category_id: int,
    category: MenuCategoryUpdate
):
    try:
        return MenuCategoryService.update_category(
            category_id,
            category
        )
    except Exception as error:
        handle_error(error)


# ---------------- MENU ITEMS ----------------

@router.post("/menu/items")
def create_menu_item(item: MenuItemCreate):
    try:
        return MenuItemService.create_menu_item(item)
    except Exception as error:
        handle_error(error)


@router.get("/menu/items/available")
def get_available_items():
    try:
        return MenuItemService.get_available_items()
    except Exception as error:
        handle_error(error)


@router.get("/menu/items/category/{category_id}")
def get_items_by_category(category_id: int):
    try:
        return MenuItemService.get_items_by_category(category_id)
    except Exception as error:
        handle_error(error)


@router.get("/menu/items")
def get_menu_items():
    try:
        return MenuItemService.get_menu_items()
    except Exception as error:
        handle_error(error)


@router.get("/menu/items/{item_id}")
def get_menu_item(item_id: int):
    try:
        return MenuItemService.get_menu_item(item_id)
    except Exception as error:
        handle_error(error)


@router.put("/menu/items/{item_id}")
def update_menu_item(
    item_id: int,
    item: MenuItemUpdate
):
    try:
        return MenuItemService.update_menu_item(
            item_id,
            item
        )
    except Exception as error:
        handle_error(error)