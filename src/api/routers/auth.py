from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from api.schemas.auth import RegisterSchema, UserResponseSchema, JWTTokenResponse
from common.constants import ACCESS_TOKEN_EXPIRE_DELTA
from core.models.user import UserModel
from core.services.user import UserService
from api.dependencies import get_db_user, get_user_service
from core.security.passwords import check_password
from core.security.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponseSchema, status_code=HTTP_201_CREATED
)
async def register_handler(
    user_service: Annotated[UserService, Depends(get_user_service)],
    data: RegisterSchema,
):
    """
    Создает нового пользователя с введенными данными

    Возвращает 400, если пользователь с таким email уже существует

    Возвращает легкую модель пользователя (id, email)
    """
    if await user_service.exists_by_email(data.email):
        raise HTTPException(
            detail="User with this email already exists",
            status_code=HTTP_400_BAD_REQUEST,
        )
    return await user_service.register(data.email, data.password)


@router.post("/token", response_model=JWTTokenResponse)
async def token_handler(
    user_service: Annotated[UserService, Depends(get_user_service)],
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    Производит oauth2 авторизацию пользователя

    Возвращает пару access_token и token_type: bearer
    """
    user = await user_service.get_by_email(data.username)
    if user is None:
        raise HTTPException(
            detail="Invalid credentials",
            status_code=HTTP_401_UNAUTHORIZED,
        )
    if not check_password(data.password, user.hashed_password):
        raise HTTPException(
            detail="Invalid credentials",
            status_code=HTTP_401_UNAUTHORIZED,
        )
    token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=ACCESS_TOKEN_EXPIRE_DELTA
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponseSchema)
async def get_me(user: UserModel = Depends(get_db_user)):
    return user
