from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from infrastructure.brokers.broker import Broker
from infrastructure.repositories.repository import Repository
from models.movements import Movement


class Infrastructure:
    repository: Repository
    _broker: Broker | None

    def __init__(self, repository: Repository, broker: Broker | None = None):
        self.repository = repository
        self._broker = broker

    async def health(self) -> bool:
        return all(
            [
                await self.repository.health(),
                await self.broker.health() if self._broker else True,
            ]
        )

    @property
    def broker(self) -> Broker:
        if not self._broker:
            raise AttributeError("Absent broker")
        return self._broker

    @staticmethod
    def ready() -> bool:
        return True

    @asynccontextmanager
    async def single_transaction(self) -> AsyncIterator["Infrastructure"]:
        async with self.repository.single_transaction() as st_repository:
            yield Infrastructure(st_repository, self.broker)

    async def getting_events(self) -> AsyncIterator[list[Movement]]:
        async for events in self.broker.getting_events():
            yield [Movement(source=event["source"], **event.get("data", {})) for event in events if event.get("data")]
