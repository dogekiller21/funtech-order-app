from uuid import UUID

from redis.asyncio import Redis
import json

from common.config import get_redis_settings
from common.shemas.order import CachedOrderScheme
from core.models.order import OrderModel
from common.config import RedisSettings


class RedisClient:
    def __init__(self, settings: RedisSettings) -> None:
        self.client = Redis.from_url(settings.get_url(), decode_responses=True)
        self.ttl = settings.ttl

    def _get_key(self, order_id: UUID) -> str:
        return f"order:{order_id}"

    def serialize(self, model: OrderModel) -> dict:
        # записываем только нужные данные (если в схеме чего-то не будет)
        data = CachedOrderScheme.model_validate(model).model_dump()
        data["id"] = str(data["id"])
        data["created_at"] = model.created_at.isoformat()
        data["updated_at"] = model.updated_at.isoformat()
        data["user_id"] = str(data["user_id"])
        data["items"] = json.dumps(data["items"])
        data["total_price"] = str(data["total_price"])
        return data

    def deserialize(self, data: dict) -> CachedOrderScheme:
        data["items"] = json.loads(data["items"])
        return CachedOrderScheme.model_validate(data)

    async def update_cache(self, model: OrderModel) -> None:
        """
        Сериализует модель и пишет ее с помощью HSET в редиску по уникальному ключу

        """
        key = self._get_key(model.id)
        value = self.serialize(model)
        await self.client.hset(key, mapping=value)  # pyright: ignore [reportGeneralTypeIssues]
        await self.client.expire(key, self.ttl)

    async def get_order_by_id(self, order_id: UUID) -> CachedOrderScheme | None:
        """
        Получает десереализованную модель из редиса

        Возвращает None, если по такому ключу модель не найдена
        """
        key = self._get_key(order_id)
        order = await self.client.hgetall(key)  # pyright: ignore [reportGeneralTypeIssues]
        if not order:
            return None

        return self.deserialize(order)


redis_client = RedisClient(settings=get_redis_settings())
