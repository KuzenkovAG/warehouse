from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from infrastructure.repositories.database import Database
from infrastructure.repositories.movements_repository import MovementsRepository
from infrastructure.repositories.warehouses_repository import WarehousesRepository


class Repository:
    def __init__(
        self,
        database: Database,
        movements_repository: MovementsRepository,
        warehouses_repository: WarehousesRepository,
    ):
        self._database = database

        self.movements = movements_repository
        self.warehouses = warehouses_repository

    async def health(self) -> bool:
        return await self._database.is_connected()

    @property
    def sub_repositories(self) -> tuple:
        return (
            self.movements,
            self.warehouses,
        )

    @asynccontextmanager
    async def single_transaction(self) -> AsyncIterator["Repository"]:
        async with self._database.single_transaction() as st_database:
            yield Repository(st_database, *[repo.override(st_database) for repo in self.sub_repositories])
