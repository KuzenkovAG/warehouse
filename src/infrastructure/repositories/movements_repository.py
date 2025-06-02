from infrastructure.repositories.base_repository import BaseRepository


class MovementsRepository(BaseRepository):
    async def add(self): ...

    async def select(self): ...
