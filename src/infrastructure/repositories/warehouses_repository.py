from sqlalchemy import and_

from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.repositories.db_models import warehouses_table
from models.product import ProductOutput, ProductFilter


class WarehousesRepository(BaseRepository):
    async def select_product(self, item: ProductFilter) -> ProductOutput | None:
        query = warehouses_table.select().where(
            and_(
                warehouses_table.c.warehouse_id == item.warehouse_id,
                warehouses_table.c.product_id == item.product_id,
                warehouses_table.c.is_active.is_(True),
            )
        )

        async with self.conn() as conn:
            row = (await conn.execute(query)).mappings().one_or_none()

        return ProductOutput(**row) if row else None
