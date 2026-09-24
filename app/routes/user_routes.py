from fastapi import APIRouter, HTTPException, status

from app.schemas.user_schema import UserCreate, UserUpdate
from app.services.service import UserService

router = APIRouter()


def handle_error(error: Exception):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(error)
    )


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate):
    try:
        return UserService.create_user(data)
    except Exception as e:
        handle_error(e)


@router.get("/users")
def get_users():
    try:
        return UserService.get_users()
    except Exception as e:
        handle_error(e)


@router.get("/users/{user_id}")
def get_user(user_id: str):
    try:
        return UserService.get_user(user_id)
    except Exception as e:
        handle_error(e)


@router.put("/users/{user_id}")
def update_user(user_id: str, data: UserUpdate):
    try:
        return UserService.update_user(user_id, data)
    except Exception as e:
        handle_error(e)


@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    try:
        return UserService.delete_user(user_id)
    except Exception as e:
        handle_error(e)