from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_schema import UserLogin, UserCreate, TokenResponse
from app.services.auth_service import AuthService
from app.routes.dependencies import handle_error, get_current_user, require_roles

router = APIRouter(tags=["Authentication"])


@router.post("/auth/login", response_model=TokenResponse)
def login(data: UserLogin):
    try:
        return AuthService.login(data.email, data.password)
    except Exception as e:
        handle_error(e)


@router.post("/users/login", response_model=TokenResponse)
def user_login_alias(data: UserLogin):
    try:
        return AuthService.login(data.email, data.password)
    except Exception as e:
        handle_error(e)


@router.post("/auth/register", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
def register(data: UserCreate):
    try:
        return AuthService.register(data)
    except Exception as e:
        handle_error(e)


@router.get("/auth/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
