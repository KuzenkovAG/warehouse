from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from utils.enums import MovementType


class BaseMovement(BaseModel):
    movement_id: UUID
    warehouse_id: UUID
    product_id: UUID
    timestamp: datetime
    event: MovementType
    quantity: int


class MovementOutput(BaseMovement):
    id: UUID
    created_at: datetime
    updated_at: datetime


class Movement(BaseMovement): ...


class MovementFilter(BaseModel):
    movement_id: UUID
