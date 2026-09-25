from bson import ObjectId
from app.database.mongodb import menu_categories_collection, menu_items_collection
from app.services.common import (
    now_utc,
    to_object_id,
    decimal128,
    serialize_document,
    serialize_documents,
)


class MenuCategoryService:

    @staticmethod
    def create_category(data):

        if menu_categories_collection.find_one(
            {"name": data.name}
        ):
            raise ValueError("Category already exists")

        category = {
            "name": data.name,
            "description": data.description,
            "created_at": now_utc(),
        }

        result = menu_categories_collection.insert_one(category)

        category["_id"] = result.inserted_id

        return serialize_document(category)

    @staticmethod
    def get_categories():

        categories = menu_categories_collection.find().sort(
            "name",
            1
        )

        return serialize_documents(categories)

    @staticmethod
    def get_category(category_id):

        category = menu_categories_collection.find_one(
            {"_id": to_object_id(category_id)}
        )

        if not category:
            raise ValueError("Category not found")

        return serialize_document(category)

    @staticmethod
    def update_category(category_id, data):

        update_data = data.model_dump(
            exclude_unset=True
        )

        result = menu_categories_collection.update_one(
            {"_id": to_object_id(category_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise ValueError("Category not found")

        return MenuCategoryService.get_category(category_id)



#menuitemservice...
class MenuItemService:

    @staticmethod
    def create_item(data):

        category = menu_categories_collection.find_one(
            {"_id": to_object_id(data.category_id)}
        )

        if not category:
            raise ValueError("Category not found")

        item = {
            "name": data.name,
            "description": data.description,
            "category_id": to_object_id(data.category_id),
            "price": decimal128(data.price),
            "preparation_time": data.preparation_time,
            "is_available": data.is_available,
            "is_vegetarian": data.is_vegetarian,
            "created_at": now_utc(),
        }

        result = menu_items_collection.insert_one(item)

        item["_id"] = result.inserted_id

        return serialize_document(item)

    @staticmethod
    def get_items():

        items = menu_items_collection.find().sort(
            "name",
            1
        )

        return serialize_documents(items)

    @staticmethod
    def get_item(item_id):

        item = menu_items_collection.find_one(
            {"_id": to_object_id(item_id)}
        )

        if not item:
            raise ValueError("Menu item not found")

        return serialize_document(item)

    @staticmethod
    def get_available_items():

        items = menu_items_collection.find(
            {"is_available": True}
        )

        return serialize_documents(items)

    @staticmethod
    def get_items_by_category(category_id):

        items = menu_items_collection.find(
            {
                "category_id": to_object_id(category_id)
            }
        )

        return serialize_documents(items)

    @staticmethod
    def update_item(item_id, data):

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "category_id" in update_data:
            update_data["category_id"] = to_object_id(
                update_data["category_id"]
            )

        if "price" in update_data:
            update_data["price"] = decimal128(
                update_data["price"]
            )

        result = menu_items_collection.update_one(
            {"_id": to_object_id(item_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise ValueError("Menu item not found")

        return MenuItemService.get_item(item_id)



#ingredientservice...
