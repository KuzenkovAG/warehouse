from sqlalchemy import Boolean, Column, DateTime, Integer, MetaData, Table
from sqlalchemy.dialects.postgresql import ENUM, UUID

from utils.enums import (
    EventType,
)

metadata = MetaData()

movements_table = Table(
    "movements",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("movement_id", UUID(as_uuid=True), nullable=False),
    Column("warehouse_id", UUID(as_uuid=True), nullable=False),
    Column("product_id", UUID(as_uuid=True), nullable=False),
    Column("timestamp", DateTime, nullable=False),
    Column("event", ENUM(EventType), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
    Column("is_active", Boolean, nullable=False),
)

warehouses_table = Table(
    "warehouses",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("warehouse_id", UUID(as_uuid=True), nullable=False),
    Column("product_id", UUID(as_uuid=True), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
    Column("is_active", Boolean, nullable=False),
)
