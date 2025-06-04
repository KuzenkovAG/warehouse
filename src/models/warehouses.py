from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.movements import Movement


class Warehouse(BaseModel):
    warehouse_id: UUID
    product_id: UUID
    quantity: int

    @classmethod
    def from_movement(cls, movement: Movement) -> "Warehouse":
        return cls(
            warehouse_id=movement.warehouse_id,
            product_id=movement.product_id,
            quantity=movement.quantity,
        )


class WarehouseFilter(BaseModel):
    warehouse_id: UUID
    product_id: UUID

    def __hash__(self):
        return hash(f"{self.warehouse_id}_{self.product_id}")


class ProductOutput(BaseModel):
    id: UUID
    warehouse_id: UUID
    product_id: UUID
    quantity: int
    created_at: datetime
    updated_at: datetime
