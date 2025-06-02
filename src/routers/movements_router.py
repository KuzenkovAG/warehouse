from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from dependencies import ViewContainer
from services.movements_service import MovementsService

router = APIRouter(prefix="/api/movements", tags=["Movements"])


@router.get(
    path="/{movement_id}",
    response_model=...,  # TODO:
    summary="Получение данных о продукте",
)
@inject
async def get(
    movement_id: UUID,
    service: MovementsService = Depends(Provide[ViewContainer.service]),
) -> ORJSONResponse: ...
