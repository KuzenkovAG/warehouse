from collections.abc import AsyncIterable

from infrastructure.brokers.kafka.kafka import Kafka


class Broker:
    kafka: Kafka

    def __init__(self, kafka: Kafka):
        self.kafka = kafka

    async def health(self) -> bool:
        return await self.kafka.health()

    async def getting_events(self) -> AsyncIterable[list[dict]]:
        async for events in self.kafka.getting_events():
            yield events
