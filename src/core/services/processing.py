from broker.producer import rabbit_producer
from common.shemas.broker import BrokerMessageSchema
from core.models.order import OrderModel
from common.shemas.order import CachedOrderScheme


async def process_order_after_creation(order: OrderModel) -> None:
    order_data = CachedOrderScheme.model_validate(order).model_dump(mode="json")
    await rabbit_producer.send_message(BrokerMessageSchema(data=order_data))
