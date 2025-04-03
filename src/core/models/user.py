from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.constants import MAX_EMAIL_LENGTH
from core.models.base import BaseModel

if TYPE_CHECKING:
    from core.models.order import OrderModel


class UserModel(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(MAX_EMAIL_LENGTH), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(64))

    orders: Mapped[list["OrderModel"]] = relationship(
        "OrderModel",
    )
