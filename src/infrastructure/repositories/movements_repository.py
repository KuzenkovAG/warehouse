import uuid
from datetime import UTC, datetime

from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import insert

from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.repositories.db_models import movements_table
from models.movements import Movement, MovementFilter, MovementOutput


class MovementsRepository(BaseRepository):
    async def add(self, movements: list[Movement]) -> None:
        dt = datetime.now(UTC).replace(tzinfo=None)
        query = insert(movements_table).values(
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

    async def select_movements(self, item: MovementFilter) -> list[MovementOutput]:
        query = movements_table.select().where(
            and_(
                movements_table.c.movement_id == item.movement_id,
                movements_table.c.is_active.is_(True),
            )
        )

        async with self.conn() as conn:
            rows = (await conn.execute(query)).mappings()

        return [MovementOutput(**row) for row in rows]
