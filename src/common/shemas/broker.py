from typing import Any

from pydantic import BaseModel, ConfigDict


class BrokerMessageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data: dict[str, Any]
