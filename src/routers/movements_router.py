from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

from dependencies import ViewContainer
from models.movements import MovementFilter, MovementOutput, MovementInfo
from services.movements_service import MovementsService

router = APIRouter(prefix="/api/movements", tags=["Movements"])


@router.get(
    path="/{movement_id}",
    summary="Получение данных о перемещении",
)
@inject
async def get(
    movement_id: UUID = Path(..., description="id перемещения"),
    service: MovementsService = Depends(Provide[ViewContainer.movements_service]),
) -> MovementInfo:
    item = MovementFilter(
        movement_id=movement_id,
    )
    return await service.get_movement(item)
