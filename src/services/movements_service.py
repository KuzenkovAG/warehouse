from infrastructure.repositories.movements_repository import MovementsRepository
from models.movements import Movement, MovementFilter, MovementOutput, MovementInfo
from services.base_service import BaseService
from settings import settings
from utils.cache import AsyncCache
from utils.http_exceptions import AbsentMovementError


class MovementsService(BaseService):
    repository: MovementsRepository

    @AsyncCache(maxsize=settings.MOVEMENT_CACHE_SIZE, ttl=settings.MOVEMENT_CACHE_EXPIRATION)
    async def get_movement(self, item: MovementFilter) -> MovementInfo:
        """Получение перемещение"""
        movements = await self.repository.select_movements(item)
        if not movements:
            raise AbsentMovementError

        return MovementInfo.from_movements(movements)

    async def save(self, movements: list[Movement]) -> None:
        """Сохранение перемещения."""
        await self.repository.add(movements)
