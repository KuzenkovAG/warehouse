from uuid import UUID

from infrastructure.repositories.movements_repository import MovementsRepository
from models.movements import Movement
from services.base_service import BaseService


class MovementsService(BaseService):
    repository: MovementsRepository

    async def get(self, movement_id: UUID): ...

    async def save(self, movements: list[Movement]) -> None:
        await self.repository.add(movements)
