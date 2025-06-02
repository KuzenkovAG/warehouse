from infrastructure.repositories.warehouses_repository import WarehousesRepository
from services.base_service import BaseService


class WarehousesService(BaseService):
    repository: WarehousesRepository

    async def get(self, item): ...

    async def save(self): ...

    async def update(self): ...
