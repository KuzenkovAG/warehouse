from infrastructure.repositories.warehouses_repository import WarehousesRepository
from models.warehouses import ProductOutput, WarehouseFilter
from services.base_service import BaseService
from utils.http_exceptions import AbsentProductError


class WarehousesService(BaseService):
    repository: WarehousesRepository

    async def get_product(self, item: WarehouseFilter) -> ProductOutput:
        product = await self.repository.select_product(item)
        if not product:
            raise AbsentProductError
        return product
