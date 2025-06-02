from contextlib import asynccontextmanager

from infrastructure.brokers.broker import Broker
from infrastructure.repositories.repository import Repository


class Infrastructure:
    repository: Repository
    broker: Broker | None

    def __init__(self, repository: Repository, broker: Broker | None = None):
        self.repository = repository
        self.broker = broker

    async def health(self) -> bool:
        return all(
            [
                await self.repository.health(),
                await self.broker.health() if self.broker else True,
            ]
        )

    @staticmethod
    def ready() -> bool:
        return True  # TODO

    @asynccontextmanager
    async def single_transaction(self):
        async with self.repository.single_transaction() as st_repository:
            yield Infrastructure(st_repository, self.broker)
