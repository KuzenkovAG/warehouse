from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql.compiler import SQLCompiler

from infrastructure.repositories.database import Database


class BaseRepository:
    @classmethod
    def override(cls, overridden_database: Database):  # noqa:ANN206
        return cls(overridden_database)

    def __init__(self, database: Database):
        self.database = database

    @asynccontextmanager
    async def single_transaction(self):  # noqa:ANN201
        async with self.database.single_transaction() as st_database:
            yield type(self)(st_database)

    @asynccontextmanager
    async def conn(self) -> AsyncIterator[AsyncConnection]:
        async with self.database.conn() as conn:
            yield conn

    @staticmethod
    def info_sql(query: Select) -> SQLCompiler:
        return query.compile(compile_kwargs={"literal_binds": True})
