
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response
from starlette_prometheus import metrics

from dependencies import VehiclesDaemonContainer, ViewContainer
from services.service import Service

router = APIRouter(tags=["System"])
router.add_route("/metrics", metrics)


@inject
async def get_service(
    view_service: Service = Depends(Provide[ViewContainer.service]),
    daemon_service: Service = Depends(Provide[VehiclesDaemonContainer.service]),
) -> Service:
    if not isinstance(view_service, Provide):
        return view_service
    elif not isinstance(daemon_service, Provide):
        return daemon_service
    raise TypeError("Got unknown service")


@router.get("/healthz")
async def health(service: Service = Depends(get_service)) -> Response:
    return Response(status_code=status.HTTP_200_OK if await service.health() else status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/readyz")
async def ready(service: Service = Depends(get_service)) -> Response:
    return Response(status_code=status.HTTP_200_OK if service.ready() else status.HTTP_500_INTERNAL_SERVER_ERROR)
