from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from utils.enums import MovementType


class Movement(BaseModel):
    movement_id: UUID
    warehouse_id: UUID
    product_id: UUID
    timestamp: datetime
    event: MovementType
    quantity: int
