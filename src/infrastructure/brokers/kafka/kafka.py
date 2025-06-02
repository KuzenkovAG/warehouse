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
