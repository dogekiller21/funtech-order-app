from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.repository.sqlalchemy.generic import GenericRepository
from core.models.order import OrderModel
from core.enums.orders import OrderStatus


class SQLAlchemyOrdersRepository(GenericRepository[OrderModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(OrderModel, session)

    async def list_by_user_id(self, user_id: UUID) -> list[OrderModel]:
        query = select(OrderModel).filter_by(user_id=user_id)
        return list((await self.session.execute(query)).scalars().all())

    async def update_status_by_id(
        self, order_id: UUID, status: OrderStatus
    ) -> OrderModel:
        query = (
            update(OrderModel)
            .where(OrderModel.id == order_id)
            .values(status=status)
            .returning(OrderModel)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one()
