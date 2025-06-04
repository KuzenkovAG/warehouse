from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

from dependencies import ViewContainer
from models.warehouses import ProductOutput, WarehouseFilter
from services.warehouses_service import WarehousesService

router = APIRouter(prefix="/api/warehouses", tags=["Warehouses"])


@router.get(
    path="/{warehouse_id}/products/{product_id}",
    summary="Получение данных о продукте",
)
@inject
async def get_product(
    warehouse_id: UUID = Path(..., description="id склада"),
    product_id: UUID = Path(..., description="id продукта"),
    service: WarehousesService = Depends(Provide[ViewContainer.warehouses_service]),
) -> ProductOutput:
    item = WarehouseFilter(
        warehouse_id=warehouse_id,
        product_id=product_id,
    )
    return await service.get_product(item)
