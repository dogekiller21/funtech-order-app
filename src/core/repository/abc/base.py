from abc import ABC, abstractmethod
from uuid import UUID


class AbstractRepository[T](ABC):
    def __init__(self, model: type[T]):
        self.model = model

    @abstractmethod
    async def get_by_id(self, obj_id: UUID) -> T | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[T]:
        pass

    @abstractmethod
    async def create(self, **kwargs) -> T | None:
        pass

    @abstractmethod
    async def update_instance(self, instance: T, **kwargs) -> T:
        pass

    @abstractmethod
    async def delete(self, instance: T) -> None:
        pass
