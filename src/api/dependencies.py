from datetime import datetime, UTC
from typing import AsyncGenerator, Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from cache.client import redis_client
from core.database import session_
from core.models.order import OrderModel
from core.services.orders import OrdersService
from core.repository.sqlalchemy.orders import SQLAlchemyOrdersRepository
from core.repository.sqlalchemy.user import SQLAlchemyUserRepository
from core.services.user import UserService
from core.security.oauth2 import oauth2_scheme
from common.datetime import get_utc_now
from core.models.user import UserModel
from core.security.jwt import decode_access_token
from common.shemas.order import CachedOrderScheme


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with session_() as session:
        try:
            yield session
        finally:
            await session.close()


def get_user_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> UserService:
    """
    Фабрика для создания сервиса пользователей
    """
    repo = SQLAlchemyUserRepository(session)
    return UserService(repo)


def get_order_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> OrdersService:
    """
    Фабрика для создания сервиса ордеров
    """
    repo = SQLAlchemyOrdersRepository(session)
    return OrdersService(repo)


async def get_db_user(
    user_service: Annotated[UserService, Depends(get_user_service)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserModel:
    """
    Получает авторизованного пользователя

    Возвращает 401, если пользователь не был авторизован
    """
    try:
        data = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            detail="Invalid token",
            status_code=HTTP_401_UNAUTHORIZED,
        )
    exp = datetime.fromtimestamp(data["exp"], tz=UTC)
    if exp < get_utc_now():
        raise HTTPException(
            detail="Invalid token",
            status_code=HTTP_401_UNAUTHORIZED,
        )
    user = await user_service.get_by_id(data["sub"])
    if user is None:
        raise HTTPException(
            detail="User not found",
            status_code=HTTP_401_UNAUTHORIZED,
        )
    return user


async def get_order_by_id(
    order_id: UUID,
    order_service: Annotated[OrdersService, Depends(get_order_service)],
) -> CachedOrderScheme:
    """
    Получает ордер по id из query params

    Возвращает 404, если ордер с таким id не найден
    """
    cached_order = await redis_client.get_order_by_id(order_id)

    if cached_order is None:
        order = await order_service.get_by_id(order_id)
        if order is None:
            raise HTTPException(
                detail="Order not found", status_code=HTTP_404_NOT_FOUND
            )
        cached_order = CachedOrderScheme.model_validate(order)
        await redis_client.update_cache(order)

    return cached_order


async def get_user_by_id(
    user_id: UUID,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserModel:
    """
    Получает пользователя по id из query params

    Возвращает 400, если пользователь с таким id не найден
    """
    user = await user_service.get_by_id(user_id)
    if user is None:
        raise HTTPException(detail="User not found", status_code=HTTP_400_BAD_REQUEST)
    return user
