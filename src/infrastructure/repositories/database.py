from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from utils.logger import exception


class Database:
    _engine: AsyncEngine | None
    _transaction: AsyncConnection | None

    def __init__(
        self,
        *,
        engine: AsyncEngine | None = None,
        transaction: AsyncConnection | None = None,
    ):
        self._engine = engine
        self._transaction = transaction

    async def is_connected(self) -> bool:
        if not self._engine:
            return False

        try:
            async with self.conn() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception:  # noqa:BLE001
            exception("PG connection error")
            return False
        return True

    @asynccontextmanager
    async def single_transaction(self) -> AsyncIterator["Database"]:
        if self._transaction and not self._transaction.closed:
            yield self
        else:
            if not self._engine:
                raise TypeError("Absent engine")
            async with self._engine.begin() as conn:
                yield Database(transaction=conn)

    @asynccontextmanager
    async def conn(self) -> AsyncIterator[AsyncConnection]:
        if self._transaction:
            yield self._transaction
        else:
            if not self._engine:
                raise TypeError("Absent engine")
            async with self._engine.begin() as conn:
                yield conn
