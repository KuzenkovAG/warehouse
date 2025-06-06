from sqlalchemy import Boolean, Column, DateTime, Integer, MetaData, String, Table
from sqlalchemy.dialects.postgresql import ENUM, UUID

from utils.enums import (
    MovementType,
)

metadata = MetaData()

movements_table = Table(
    "movements",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("movement_id", UUID(as_uuid=True), nullable=False, index=True),
    Column("warehouse_id", UUID(as_uuid=True), nullable=False),
    Column("source", String, nullable=False),
    Column("product_id", UUID(as_uuid=True), nullable=False),
    Column("timestamp", DateTime(timezone=True), nullable=False),
    Column("event", ENUM(MovementType), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
    Column("is_active", Boolean, nullable=False),
)

warehouses_table = Table(
    "warehouses",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("warehouse_id", UUID(as_uuid=True), nullable=False),
    Column("product_id", UUID(as_uuid=True), nullable=False, index=True),
    Column("quantity", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
    Column("is_active", Boolean, nullable=False),
)
