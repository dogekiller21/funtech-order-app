from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from core.enums.orders import OrderStatus


class CachedOrderScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field()
    created_at: datetime
    updated_at: datetime

    user_id: UUID
    items: dict[str, str | int]
    total_price: float
    status: OrderStatus
