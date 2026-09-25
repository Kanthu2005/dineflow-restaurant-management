from decimal import Decimal
from bson import ObjectId
from bson.decimal128 import Decimal128
from app.database.mongodb import ingredients_collection
from app.services.common import (
    now_utc,
    to_object_id,
    decimal128,
    serialize_document,
    serialize_documents,
)


class IngredientService:

    @staticmethod
    def create_ingredient(data):

        if ingredients_collection.find_one(
            {"name": data.name}
        ):
            raise ValueError("Ingredient already exists")

        ingredient = {
            "name": data.name,
            "unit": data.unit,
            "available_quantity": decimal128(
                data.available_quantity
            ),
            "minimum_stock_level": decimal128(
                data.minimum_stock_level
            ),
            "cost_per_unit": decimal128(
                data.cost_per_unit
            ),
            "supplier_name": data.supplier_name,
            "is_active": data.is_active,
            "created_at": now_utc(),
        }

        result = ingredients_collection.insert_one(
            ingredient
        )

        ingredient["_id"] = result.inserted_id

        return serialize_document(ingredient)

    @staticmethod
    def get_ingredients():

        ingredients = ingredients_collection.find().sort(
            "name",
            1
        )

        return serialize_documents(ingredients)

    @staticmethod
    def get_active_ingredients():

        ingredients = ingredients_collection.find(
            {"is_active": True}
        )

        return serialize_documents(ingredients)

    @staticmethod
    def get_ingredient(ingredient_id):

        ingredient = ingredients_collection.find_one(
            {"_id": to_object_id(ingredient_id)}
        )

        if not ingredient:
            raise ValueError("Ingredient not found")

        return serialize_document(ingredient)

    @staticmethod
    def update_ingredient(ingredient_id, data):

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field in [
            "minimum_stock_level",
            "cost_per_unit",
        ]:
            if field in update_data:
                update_data[field] = decimal128(
                    update_data[field]
                )

        result = ingredients_collection.update_one(
            {"_id": to_object_id(ingredient_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise ValueError("Ingredient not found")

        return IngredientService.get_ingredient(
            ingredient_id
        )

    @staticmethod
    def update_stock(ingredient_id, quantity):

        result = ingredients_collection.update_one(
            {"_id": to_object_id(ingredient_id)},
            {
                "$inc": {
                    "available_quantity": decimal128(
                        quantity
                    )
                }
            }
        )

        if result.matched_count == 0:
            raise ValueError("Ingredient not found")

        return IngredientService.get_ingredient(
            ingredient_id
        )

    @staticmethod
    def get_stock_status(ingredient_id):

        ingredient = IngredientService.get_ingredient(
            ingredient_id
        )

        available = ingredient["available_quantity"]
        minimum = ingredient["minimum_stock_level"]

        if available <= 0:
            status = "OUT_OF_STOCK"
        elif available <= minimum:
            status = "CRITICAL"
        elif available <= minimum * Decimal("1.5"):
            status = "LOW"
        else:
            status = "NORMAL"

        return {
            "ingredient_id": ingredient_id,
            "ingredient_name": ingredient["name"],
            "available_quantity": available,
            "minimum_stock_level": minimum,
            "status": status,
        }



#recipeservice...
