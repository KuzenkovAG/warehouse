import asyncio
from collections.abc import Callable

from dependency_injector.containers import DeclarativeContainer
from fastapi import FastAPI

from settings import settings
from utils.logger import info


def create_application(
    lifespan: Callable,
    inject_dependencies: Callable | None = None,
    add_middleware: Callable | None = None,
    add_handlers: Callable | None = None,
    include_routers: Callable | None = None,
) -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        docs_url=settings.SWAGGER_PATH,
        lifespan=lifespan,
    )

    if inject_dependencies:
        application.container = inject_dependencies()  # type:ignore[attr-defined]

    if add_middleware:
        add_middleware(application)

    if add_handlers:
        add_handlers(application)

    if include_routers:
        include_routers(application)

    return application


async def init_daemons(container: DeclarativeContainer) -> dict[str, asyncio.Task]:
    daemons: dict[str, asyncio.Task] = {}

    await container.init_resources()  # type: ignore[misc]

    for daemon in await container.daemons.init():  # type: ignore[misc, attr-defined]
        daemons[daemon.__name__] = asyncio.create_task(daemon)
        info(f"Daemon: {daemon.__name__} is working")

    return daemons


async def shutdown_resources(
    daemons: dict[str, asyncio.Task],
    container: DeclarativeContainer,
) -> None:
    for daemon_name, daemon in daemons.items():
        daemon.cancel()
        try:
            await daemon
        except asyncio.CancelledError:
            info(f"Daemon: {daemon_name} was stopped")

    await container.shutdown_resources()  # type: ignore[misc]
