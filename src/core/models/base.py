from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlalchemy import MetaData, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
    orm_insert_sentinel,
    validates,
)

from common.datetime import get_utc_now
from core.models.defaults import ServerDefault

convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


class Base(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(naming_convention=convention)


class BaseModel(Base):
    # Базовая модель для наследования
    __abstract__ = True

    # alembic сам нормально определит тип
    id: Mapped[UUID] = mapped_column(
        primary_key=True, default=uuid4, server_default=ServerDefault.uuid
    )

    # Информационные поля для более детальной информации о записях
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utc_now,
        server_default=ServerDefault.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utc_now,
        server_default=ServerDefault.now,
        onupdate=get_utc_now,
        server_onupdate=ServerDefault.now,
    )

    @declared_attr
    def _sentinel(cls) -> Mapped[int]:
        return orm_insert_sentinel(name="sa_orm_sentinel")

    @validates("created_at", "updated_at")
    def force_aware(self, _: str, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value
