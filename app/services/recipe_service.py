from bson import ObjectId
from app.database.mongodb import (
    recipes_collection,
    menu_items_collection,
    ingredients_collection,
)
from app.services.common import (
    now_utc,
    to_object_id,
    decimal128,
    serialize_document,
    serialize_documents,
)


class RecipeService:

    @staticmethod
    def create_recipe(menu_item_id, data):

        menu_item = menu_items_collection.find_one(
            {"_id": to_object_id(menu_item_id)}
        )

        if not menu_item:
            raise ValueError("Menu item not found")

        ingredient = ingredients_collection.find_one(
            {"_id": to_object_id(data.ingredient_id)}
        )

        if not ingredient:
            raise ValueError("Ingredient not found")

        existing = recipes_collection.find_one(
            {
                "menu_item_id": to_object_id(menu_item_id),
                "ingredient_id": to_object_id(
                    data.ingredient_id
                ),
            }
        )

        if existing:
            raise ValueError(
                "Ingredient already exists in recipe"
            )

        recipe = {
            "menu_item_id": to_object_id(menu_item_id),
            "ingredient_id": to_object_id(
                data.ingredient_id
            ),
            "quantity_required": decimal128(
                data.quantity_required
            ),
        }

        result = recipes_collection.insert_one(recipe)

        recipe["_id"] = result.inserted_id

        return serialize_document(recipe)

    @staticmethod
    def get_by_menu_item(menu_item_id):
        recipes = recipes_collection.find(
            {
                "menu_item_id": to_object_id(
                    menu_item_id
                )
            }
        )
        return serialize_documents(recipes)

    @staticmethod
    def get_recipe(recipe_id):
        recipe = recipes_collection.find_one(
            {"_id": to_object_id(recipe_id)}
        )
        if not recipe:
            raise ValueError("Recipe not found")
        return serialize_document(recipe)

    @staticmethod
    def get_recipe_by_id(recipe_id):
        return RecipeService.get_recipe(recipe_id)

    @staticmethod
    def update_recipe(recipe_id, data):
        result = recipes_collection.update_one(
            {"_id": to_object_id(recipe_id)},
            {
                "$set": {
                    "quantity_required": decimal128(
                        data.quantity_required
                    )
                }
            }
        )
        if result.matched_count == 0:
            raise ValueError("Recipe not found")
        return RecipeService.get_recipe(recipe_id)


# ============================================================
# 7. TABLE SERVICE
# ============================================================
