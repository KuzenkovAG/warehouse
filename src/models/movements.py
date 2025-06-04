from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from utils.enums import MovementType


class Warehouse(BaseModel):
    source: str
    warehouse_id: UUID


class BaseMovement(BaseModel):
    movement_id: UUID
    warehouse_id: UUID
    product_id: UUID
    timestamp: datetime
    event: MovementType
    source: str
    quantity: int


class MovementOutput(BaseMovement):
    id: UUID
    created_at: datetime
    updated_at: datetime


class Movement(BaseMovement): ...


class MovementFilter(BaseModel):
    movement_id: UUID

    def __hash__(self):
        return hash(str(self.movement_id))


class MovementInfo(BaseModel):
    sender: Warehouse | None = None
    receiver: Warehouse | None = None
    product_id: UUID
    quantity: int
    send_dt: datetime | None = None
    receive_dt: datetime | None = None
    delivery_time_sec: int | None = None

    @classmethod
    def from_movements(cls, movements: list[MovementOutput]) -> "MovementInfo":
        """
        Объединение перемещений (отправки и поступления) в одно

        :param movements: Перемещения
        :return: Объединенный результат
        """

        arrivals = [movement for movement in movements if movement.event == MovementType.arrival]
        departures = [movement for movement in movements if movement.event == MovementType.departure]

        arrival = arrivals[0] if arrivals else None
        departure = departures[0] if departures else None

        return cls(
            sender={"source": departure.source, "warehouse_id": departure.warehouse_id} if departure else None,
            receiver={"source": arrival.source, "warehouse_id": arrival.warehouse_id} if arrival else None,
            product_id=arrival.product_id if arrival else departure.product_id,
            quantity=arrival.quantity if arrival else departure.quantity,
            send_dt=departure.timestamp if departure else None,
            receive_dt=arrival.timestamp if arrival else None,
            delivery_time_sec=(arrival.timestamp - departure.timestamp).seconds if arrival and departure else None,
        )
