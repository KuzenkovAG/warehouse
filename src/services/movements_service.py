from infrastructure.repositories.movements_repository import MovementsRepository
from models.movements import Movement, MovementFilter, MovementOutput
from services.base_service import BaseService
from utils.http_exceptions import AbsentMovementError


class MovementsService(BaseService):
    repository: MovementsRepository

    async def get_movement(self, item: MovementFilter) -> list[MovementOutput]:
        movements = await self.repository.select(item)
        if not movements:
            raise AbsentMovementError
        return movements

    async def save(self, movements: list[Movement]) -> None:
        await self.repository.add(movements)
