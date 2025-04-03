from uuid import UUID

from common.shemas.order import CachedOrderScheme
from core.enums.orders import OrderStatus
from core.repository.sqlalchemy.orders import SQLAlchemyOrdersRepository
from core.models.order import OrderModel


class OrdersService:
    def __init__(self, order_repo: SQLAlchemyOrdersRepository):
        self.order_repo = order_repo

    async def get_by_id(self, id_: UUID) -> OrderModel | None:
        return await self.order_repo.get_by_id(id_)

    async def create(
        self, items: dict[str, str | int], total_price: float, user_id: UUID
    ) -> OrderModel:
        return await self.order_repo.create(
            items=items,
            total_price=total_price,
            user_id=user_id,
        )

    async def update_status(self, order_id: UUID, status: OrderStatus) -> OrderModel:
        return await self.order_repo.update_status_by_id(
            order_id=order_id, status=status
        )

    async def list_by_user_id(self, user_id: UUID) -> list[OrderModel]:
        return await self.order_repo.list_by_user_id(user_id)
