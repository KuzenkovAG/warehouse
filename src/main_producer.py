import asyncio
import random
import uuid
from datetime import datetime
from typing import Any

import orjson
from aiokafka import AIOKafkaProducer
from asyncpg.pgproto.pgproto import timedelta

from settings import settings

PRODUCTS = [
    "675e5a9b-c02e-4785-8d0a-360b163077c9",
    "bda756a0-3d02-4606-bdea-1a7e01d8f4ac",
    "955e934a-691f-4c5b-9cf1-6c434d02272d",
    "92e8b000-4474-47b5-a811-8232393ae6e3",
    "9ced56d7-fd1c-4f61-858b-bb4ecbc8713a",
]
WAREHOUSES = [
    "7d5bbb85-f0e3-48ef-b958-11d9816d65f0",
    "5f9f65f6-3d9f-4c6b-b6f4-293dafa0ec6f",
    "18792e65-40ea-4f36-b988-8ce975fd7731",
    "8943b17f-4e0a-4906-9dc1-e8715a3f43ca",
    "08ff8a3e-53a8-431e-aafc-5ad420b919c4",
]
QUANTITY = list(range(1, 100))


def _gen_message(
    movement_id: uuid.UUID,
    product_id: str,
    warehouse_id: str,
    quantity: int,
    event: str,
    time_: datetime,
) -> dict[str, Any]:
    id_ = uuid.uuid4()
    return {
        "id": id_,
        "source": "WH-3423",
        "specversion": "1.0",
        "type": "ru.retail.warehouses.movement",
        "datacontenttype": "application/json",
        "dataschema": "ru.retail.warehouses.movement.v1.0",
        "time": time_.timestamp(),
        "subject": "WH-3423:ARRIVAL",
        "destination": "ru.retail.warehouses",
        "data": {
            "movement_id": movement_id,
            "warehouse_id": warehouse_id,
            "timestamp": time_.isoformat(),
            "event": event,
            "product_id": product_id,
            "quantity": quantity,
        },
    }


def get_messages() -> list[dict]:
    movement_id = uuid.uuid4()
    product_id = random.choice(PRODUCTS)  # noqa:S311
    warehouse_id_dep = random.choice(WAREHOUSES)  # noqa:S311
    warehouse_id_arr = random.choice([wh for wh in WAREHOUSES if wh != warehouse_id_dep])  # noqa:S311
    quantity = random.choice(QUANTITY)  # noqa:S311

    send_time = datetime.now()
    receive_time = send_time + timedelta(seconds=253)

    return [
        _gen_message(movement_id, product_id, warehouse_id_dep, quantity, "departure", send_time),
        _gen_message(movement_id, product_id, warehouse_id_arr, quantity, "arrival", receive_time),
    ]


async def send_message(producer: AIOKafkaProducer) -> None:
    while True:
        try:
            messages = get_messages()
            for msg in messages:
                await producer.send_and_wait(
                    topic=settings.KAFKA_READING_TOPICS[0],
                    value=orjson.dumps(msg),
                )
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("stop send message")  # noqa:T201
            break


async def main() -> None:
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP,
    )

    await producer.start()
    try:
        await send_message(producer)
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
