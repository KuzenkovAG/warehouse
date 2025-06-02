from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from infrastructure.repositories.base_repository import BaseRepository


class BaseService:
    @classmethod
    def override(cls, overridden_repository: BaseRepository) -> "BaseService":
        return cls(overridden_repository)

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    @asynccontextmanager
    async def st_service(self) -> AsyncGenerator:
        async with self.repository.single_transaction() as st_repo:
            yield type(self)(st_repo)
