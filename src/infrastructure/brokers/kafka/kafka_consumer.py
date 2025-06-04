from aiokafka import AIOKafkaConsumer, ConsumerRecord, TopicPartition

from settings import settings


class KafkaConsumer:
    def __init__(self, consumer: AIOKafkaConsumer):
        self.consumer = consumer

    def is_connected(self) -> bool:
        return not self.consumer._closed  # noqa:SLF001

    async def get_batch(self) -> dict[TopicPartition, list[ConsumerRecord]]:
        """Получает батч сообщений."""
        return await self.consumer.getmany(
            timeout_ms=settings.KAFKA_TIMEOUT_MS,
            max_records=settings.KAFKA_BATCH_SIZE,
        )
