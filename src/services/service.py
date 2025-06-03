from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from infrastructure.infrastructure import Infrastructure
from models.movements import Movement
from services.movements_service import MovementsService
from services.warehouses_service import WarehousesService
from utils.daemon import Daemon


class Service:
    def __init__(
        self,
        infrastructure: Infrastructure,
        movements_service: MovementsService,
        warehouse_service: WarehousesService,
    ):
        self.infra = infrastructure

        self.movements = movements_service
        self.warehouse = warehouse_service

    @property
    def sub_services(self) -> tuple:
        return (
            self.movements,
            self.warehouse,
        )

    @asynccontextmanager
    async def st_service(self) -> AsyncIterator["Service"]:
        st_infrastructure: Infrastructure

        async with self.infra.single_transaction() as st_infrastructure:
            yield Service(
                st_infrastructure,
                *[
                    service.override(st_repository)
                    for service, st_repository in zip(
                        self.sub_services,
                        st_infrastructure.repository.sub_repositories,
                        strict=False,
                    )
                ],
            )

    # ---------- Daemon logic ----------

    @Daemon()
    async def starting_saving_events(self) -> None:
        """Запуск задачи на подключение к очереди и получение сообщений из очереди."""
        async for movements in self.infra.getting_events():
            await self.handle_movements(movements)

    async def handle_movements(self, movements: list[Movement]) -> None:
        """Обработка полученных событий перемещений продуктов."""
        st_service: Service

        async with self.st_service() as st_service:
            await st_service.movements.save(movements)

    # ---------- Kubernetes logic ----------

    def ready(self) -> bool:
        return self.infra.ready()

    async def health(self) -> bool:
        return await self.infra.health()
