from infrastructure.repositories.warehouses_repository import WarehousesRepository
from models.product import ProductOutput, ProductFilter
from services.base_service import BaseService
from settings import settings
from utils.cache import AsyncCache
from utils.http_exceptions import AbsentProductError


class WarehousesService(BaseService):
    repository: WarehousesRepository

    @AsyncCache(maxsize=settings.PRODUCT_CACHE_SIZE, ttl=settings.PRODUCT_CACHE_EXPIRATION)
    async def get_product(self, item: ProductFilter) -> ProductOutput:
        """Получение продукта"""
        product = await self.repository.select_product(item)
        if not product:
            raise AbsentProductError
        return product
