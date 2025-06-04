from collections.abc import AsyncIterable
from uuid import UUID

import orjson
from aiokafka import ConsumerRecord

from infrastructure.brokers.kafka.kafka_consumer import KafkaConsumer


class Kafka:
    def __init__(self, consumer: KafkaConsumer):
        self.consumer = consumer

    @staticmethod
    def _decode(msg: ConsumerRecord) -> tuple[UUID | None, dict]:
        return UUID(msg.key.decode()) if msg.key else None, orjson.loads(msg.value)

    async def getting_events(self) -> AsyncIterable[list[dict]]:
        """Получение сообщений батчами."""
        while True:
            results = await self.consumer.get_batch()
            for messages in results.values():
                yield [orjson.loads(msg.value) for msg in messages]
