from uuid import UUID

from pydantic import BaseModel

from core.enums.orders import OrderStatus


class OrderResponseSchema(BaseModel):
    id: UUID
    user_id: UUID
    items: dict[str, str | int]
    total_price: float
    status: OrderStatus


class OrderRequestSchema(BaseModel):
    items: dict[str, str | int]
    total_price: float


class OrderPatchSchema(BaseModel):
    status: OrderStatus
