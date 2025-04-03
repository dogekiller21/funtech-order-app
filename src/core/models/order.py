from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, FLOAT, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.enums.orders import OrderStatus
from core.models.base import BaseModel
from core.models.defaults import OnDelete, ServerDefault

if TYPE_CHECKING:
    from core.models.user import UserModel


class OrderModel(BaseModel):
    __tablename__ = "orders"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete=OnDelete.cascade)
    )
    items: Mapped[dict] = mapped_column(
        JSONB, default=dict, server_default=ServerDefault.empty_dict
    )
    total_price: Mapped[float] = mapped_column(
        FLOAT,
        nullable=False,
    )
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING
    )

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="orders")
