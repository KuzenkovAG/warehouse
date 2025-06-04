from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Product(BaseModel):
    warehouse_id: UUID
    product_id: UUID
    quantity: int


class ProductFilter(BaseModel):
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
