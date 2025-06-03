import uuid
from datetime import UTC, datetime

from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.repositories.db_models import movements_table
from models.movements import Movement


class MovementsRepository(BaseRepository):
    async def add(self, movements: list[Movement]):
        dt = datetime.now(UTC).replace(tzinfo=None)
        query = movements_table.insert().values(
            [
                {
                    "id": uuid.uuid4(),
                    "created_at": dt,
                    "updated_at": dt,
                    "is_active": True,
                }
                | movement.model_dump()
                for movement in movements
            ]
        )

        async with self.conn() as conn:
            await conn.execute(query)

    async def select(self): ...
