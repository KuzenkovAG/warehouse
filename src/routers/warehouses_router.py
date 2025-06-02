from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from dependencies import ViewContainer
from services.warehouses_service import WarehousesService

router = APIRouter(prefix="/api/warehouses", tags=["Warehouses"])


@router.get(
    path="/{warehouse_id}/products/{product_id}",
    response_model=...,  # TODO:
    summary="Получение данных о продукте",
)
@inject
async def get(
    warehouse_id: UUID,
    product_id: UUID,
    service: WarehousesService = Depends(Provide[ViewContainer.service]),
) -> ORJSONResponse: ...
