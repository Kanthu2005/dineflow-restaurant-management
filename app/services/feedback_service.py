from decimal import Decimal
from bson import ObjectId
from bson.decimal128 import Decimal128
from app.database.mongodb import customer_feedback_collection, orders_collection
from app.services.common import (
    now_utc,
    to_object_id,
    decimal128,
    serialize_document,
    serialize_documents,
)


class FeedbackService:

    @staticmethod
    def create_feedback(order_id, data):

        order = orders_collection.find_one(
            {"_id": to_object_id(order_id)}
        )

        if not order:
            raise ValueError("Order not found")

        existing = customer_feedback_collection.find_one(
            {
                "order_id": order["_id"],
                "customer_id": to_object_id(
                    data.customer_id
                ),
            }
        )

        if existing:
            raise ValueError(
                "Feedback already submitted for this order"
            )

        feedback = {
            "order_id": order["_id"],
            "customer_id": to_object_id(
                data.customer_id
            ),
            "rating": data.rating,
            "food_rating": data.food_rating,
            "service_rating": data.service_rating,
            "comments": data.comments,
            "created_at": now_utc(),
        }

        result = customer_feedback_collection.insert_one(
            feedback
        )

        feedback["_id"] = result.inserted_id

        return serialize_document(feedback)

    @staticmethod
    def get_feedback(feedback_id):

        feedback = customer_feedback_collection.find_one(
            {"_id": to_object_id(feedback_id)}
        )

        if not feedback:
            raise ValueError("Feedback not found")

        return serialize_document(feedback)

    @staticmethod
    def get_customer_feedback(customer_id):

        feedback = customer_feedback_collection.find(
            {
                "customer_id": to_object_id(
                    customer_id
                )
            }
        ).sort(
            "created_at",
            -1
        )

        return serialize_documents(feedback)

    @staticmethod
    def get_order_feedback(order_id):

        feedback = customer_feedback_collection.find(
            {
                "order_id": to_object_id(order_id)
            }
        )

        return serialize_documents(feedback)

    @staticmethod
    def get_all_feedback():

        feedback = customer_feedback_collection.find().sort(
            "created_at",
            -1
        )

        return serialize_documents(feedback)

    @staticmethod
    def get_summary():

        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_feedback": {
                        "$sum": 1
                    },
                    "average_rating": {
                        "$avg": "$rating"
                    },
                    "average_food_rating": {
                        "$avg": "$food_rating"
                    },
                    "average_service_rating": {
                        "$avg": "$service_rating"
                    },
                }
            }
        ]

        result = list(
            customer_feedback_collection.aggregate(
                pipeline
            )
        )

        if not result:
            return {
                "total_feedback": 0,
                "average_rating": 0,
                "average_food_rating": 0,
                "average_service_rating": 0,
            }

        summary = result[0]

        return {
            "total_feedback":
                summary["total_feedback"],
            "average_rating":
                round(summary["average_rating"], 2),
            "average_food_rating":
                round(
                    summary["average_food_rating"],
                    2
                ),
            "average_service_rating":
                round(
                    summary["average_service_rating"],
                    2
                ),
        }
