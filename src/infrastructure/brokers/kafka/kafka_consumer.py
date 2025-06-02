import asyncio

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import UnknownMemberIdError

from settings import settings
from utils.logger import info


class KafkaConsumer:
    def __init__(self, consumer: AIOKafkaConsumer):
        self.consumer = consumer

    def is_connected(self):
        return not self.consumer._closed

    async def consume(self):
        try:
            async for msg in self.consumer:
                yield msg
        except asyncio.CancelledError:
            info("Cancel consume")
            raise
        except UnknownMemberIdError as e:
            raise e

    async def commit(self, data: dict):
        """
        Подтверждает смещение.

        :param data: Данные о смещении.
        :return: None
        """
        await self.consumer.commit(data)

    async def get_batch(self):
        """Получает батч сообщений."""
        return await self.consumer.getmany(
            timeout_ms=settings.KAFKA_TIMEOUT_MS,
            max_records=settings.KAFKA_BATCH_SIZE,
        )
