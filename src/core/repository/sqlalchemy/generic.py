from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.base import BaseModel
from core.repository.abc.base import AbstractRepository

type T = BaseModel


class GenericRepository[T](AbstractRepository[T]):
    def __init__(self, model: type[T], session: AsyncSession):
        super().__init__(model)
        self.session = session

    async def get_by_id(self, obj_id: UUID) -> T | None:
        query = select(self.model).where(self.model.id == obj_id)
        return (await self.session.execute(query)).scalar_one_or_none()

    async def list_all(self) -> list[T]:
        query = select(self.model)
        return list((await self.session.execute(query)).scalars().all())

    async def create(self, **kwargs) -> T:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update_instance(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: T) -> None:
        query = delete(self.model).where(self.model.id == instance.id)
        await self.session.execute(query)
        await self.session.commit()
