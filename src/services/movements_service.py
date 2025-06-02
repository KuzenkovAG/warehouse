from uuid import UUID

from infrastructure.repositories.movements_repository import MovementsRepository
from services.base_service import BaseService


class MovementsService(BaseService):
    repository: MovementsRepository

    async def get(self, movement_id: UUID): ...

    async def save(self): ...
