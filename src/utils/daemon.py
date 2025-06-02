import asyncio
from asyncio import iscoroutinefunction
from collections.abc import Callable
from functools import wraps
from typing import Any

from settings import settings
from utils.logger import exception


class Daemon:
    """Обертка для демона, позволяет запускать функции в бесконечном режиме."""

    _restart_sec: int = settings.DAEMON_RESTART_SEC  # время перезапуска демона при ошибке

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> None:
            while True:
                try:
                    if iscoroutinefunction(func):
                        await func(*args, **kwargs)
                    else:
                        func(*args, **kwargs)
                    break
                except Exception as exc:  # noqa:BLE001
                    exception(f"DAEMON {func.__name__} FAILED [{exc}]")
                    await asyncio.sleep(self._restart_sec)

        return wrapper
