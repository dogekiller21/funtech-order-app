import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends

from api.schemas.orders import OrderPatchSchema
from cache.client import redis_client
from common.shemas.order import CachedOrderScheme
from core.models.user import UserModel
from api.dependencies import (
    get_db_user,
    get_order_by_id,
    get_order_service,
    get_user_by_id,
)
from api.schemas.orders import OrderResponseSchema, OrderRequestSchema
from core.services.orders import OrdersService
from core.services.processing import process_order_after_creation

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/{order_id:uuid}", response_model=OrderResponseSchema)
async def get_order_handler(
    order: Annotated[CachedOrderScheme, Depends(get_order_by_id)],
):
    """
    Возвращает 404, если ордер с предоставленным id не найден

    Возвращает ордер по id
    """
    return order


@router.post("/", response_model=OrderResponseSchema)
async def create_order_handler(
    data: OrderRequestSchema,
    user: Annotated[UserModel, Depends(get_db_user)],
    order_service: Annotated[OrdersService, Depends(get_order_service)],
):
    """
    Добавляет новый ордер для авторизованного пользователя

    Возвращает 401, если пользователь не авторизован или его ключ истек

    Возвращает созданный ордер
    """
    order = await order_service.create(
        user_id=user.id, items=data.items, total_price=data.total_price
    )
    asyncio.create_task(process_order_after_creation(order))
    await redis_client.update_cache(order)
    return order


@router.patch("/{order_id:uuid}", response_model=OrderResponseSchema)
async def update_order_handler(
    order: Annotated[CachedOrderScheme, Depends(get_order_by_id)],
    data: OrderPatchSchema,
    order_service: Annotated[OrdersService, Depends(get_order_service)],
):
    """
    Обновляет статус ордера

    Возвращает 404, если ордера с таким id не существует

    Возвращает обновленный ордер
    """
    updated_order = await order_service.update_status(order.id, data.status)
    await redis_client.update_cache(updated_order)
    return updated_order


@router.get("/user/{user_id:uuid}", response_model=list[OrderResponseSchema])
async def get_user_order_handlers(
    user: Annotated[UserModel, Depends(get_user_by_id)],
    order_service: Annotated[OrdersService, Depends(get_order_service)],
):
    """
    Возвращает все ордера пользователя

    Возвращает 400, если пользователя не существует

    Возвращает список с ордерами
    """
    return await order_service.list_by_user_id(user.id)
