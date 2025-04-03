import asyncio
import json

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from common.config import RabbitMQSettings, get_rabbitmq_settings
from common.shemas.broker import BrokerMessageSchema
from worker.tasks.orders import process_order


class RabbitMQConsumer:
    def __init__(self, settings: RabbitMQSettings):
        self.url = settings.get_url()
        self.queue = settings.queue
        self.prefetch_count = settings.prefetch_count
        self._connection = None
        self._channel = None
        self._queue = None

    async def handle_new_order_message(self, data: BrokerMessageSchema) -> None:
        print(f"Got new order message: {data}")
        process_order.delay(data.data)

    async def _on_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            try:
                data = json.loads(message.body.decode())
                data_model = BrokerMessageSchema.model_validate(data)
                await self.handle_new_order_message(data_model)
            except Exception as e:
                print(f"Error while processing message: {e}")
                pass

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self.url)
        self._channel = await self._connection.channel()
        self._queue = await self._channel.declare_queue(self.queue, durable=True)
        await self._channel.set_qos(prefetch_count=self.prefetch_count)

        await self._queue.consume(self._on_message)

        # держит луп
        try:
            await asyncio.Future()
        finally:
            await self.close()

    async def close(self) -> None:
        if self._connection is not None:
            await self._connection.close()


rabbit_consumer = RabbitMQConsumer(get_rabbitmq_settings())
