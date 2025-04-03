from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import UserModel
from core.repository.sqlalchemy.generic import GenericRepository


class SQLAlchemyUserRepository(GenericRepository[UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserModel, session)

    async def get_by_email(self, email: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.email == email)
        return (await self.session.execute(query)).scalar_one_or_none()

    async def exists_by_email(self, email: str) -> bool:
        query = select(exists().where(UserModel.email == email))
        result = (await self.session.execute(query)).scalar()
        return result or False
