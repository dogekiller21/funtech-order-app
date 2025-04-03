from uuid import UUID

from core.security.passwords import get_password_hash
from core.models.user import UserModel
from core.repository.sqlalchemy.user import SQLAlchemyUserRepository


class UserService:
    def __init__(self, user_repo: SQLAlchemyUserRepository):
        self.user_repo = user_repo

    async def register(self, email: str, password: str) -> UserModel | None:
        """
        Создает пользователя и хэширует пароль

        ! НЕ производит никаких проверок
        """
        user = await self.user_repo.create(
            email=email, hashed_password=get_password_hash(password)
        )
        return user

    async def exists_by_email(self, email: str) -> bool:
        return await self.user_repo.exists_by_email(email)

    async def get_by_email(self, email: str) -> UserModel | None:
        return await self.user_repo.get_by_email(email)

    async def get_by_id(self, id_: UUID) -> UserModel | None:
        return await self.user_repo.get_by_id(id_)
