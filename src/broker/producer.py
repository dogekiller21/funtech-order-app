import json
from typing import Any

import aio_pika

from common.config import RabbitMQSettings, get_rabbitmq_settings
from common.shemas.broker import BrokerMessageSchema


class RabbitMQProducer:
    def __init__(self, settings: RabbitMQSettings):
        self.url = settings.get_url()
        self.queue = settings.queue
        self._connection = None
        self._channel = None

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self.url)
        self._channel = await self._connection.channel()
        await self._channel.declare_queue(self.queue, durable=True)

    async def send_message(self, message: BrokerMessageSchema) -> None:
        if self._channel is None:
            raise RuntimeError("Connection for producer is not established")

        message_body = json.dumps(message.model_dump())

        await self._channel.default_exchange.publish(
            aio_pika.Message(
                body=message_body.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type="application/json",
            ),
            routing_key=self.queue,
        )

    async def close(self) -> None:
        if self._connection is not None:
            await self._connection.close()


rabbit_producer = RabbitMQProducer(get_rabbitmq_settings())
