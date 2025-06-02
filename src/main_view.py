from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from application import create_application, init_daemons, shutdown_resources
from dependencies import ConsumerContainer
from routers import system_router
from utils.logger import info


def add_middleware(application: FastAPI) -> None:
    from starlette_prometheus import PrometheusMiddleware

    application.add_middleware(PrometheusMiddleware)


def include_routers(application: FastAPI) -> None:
    application.include_router(system_router.router)


def inject_dependencies() -> ConsumerContainer:
    container = ConsumerContainer()
    container.check_dependencies()

    container.wire(modules=[system_router])
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
