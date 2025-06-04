from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from application import create_application, init_daemons, shutdown_resources
from dependencies import ViewContainer
from routers.routers import routers
from utils.http_exceptions import set_exceptions_handler
from utils.logger import info


def add_middleware(application: FastAPI) -> None:
    from starlette_prometheus import PrometheusMiddleware

    application.add_middleware(PrometheusMiddleware)

    set_exceptions_handler(application)


def include_routers(application: FastAPI) -> None:
    for router in routers:
        application.include_router(router.router)


def inject_dependencies() -> ViewContainer:
    container = ViewContainer()
    container.check_dependencies()

    container.wire(modules=routers)
    return container


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    info("Application starting ...")
    container = app.container  # type:ignore[attr-defined]
    daemons = await init_daemons(container)

    yield

    info("Application shutdown ...")
    await shutdown_resources(daemons, container)


app: FastAPI = create_application(
    lifespan=lifespan,
    inject_dependencies=inject_dependencies,
    add_middleware=add_middleware,
    include_routers=include_routers,
)
