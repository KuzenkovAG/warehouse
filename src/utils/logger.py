import sys
from collections.abc import Callable
from typing import Any

from loguru import logger

from settings import settings

simple_formatter = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
    "[<cyan>{name}</cyan>] "
    "<level>{level.icon} {level}</level>: "
    "<level>{message}</level> "
)

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format=simple_formatter,
    enqueue=True,
    backtrace=True,
    diagnose=True,
    level=settings.LOG_LEVEL,
)


def property_logger(func: Callable) -> Any:
    @property  # type: ignore[misc]
    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa:PLR0206
        result = func(*args, **kwargs)
        if not result:
            msg = f"Probe {func.__name__} from {func.__module__} return {result}"
            logger.debug(msg)
        return result

    return wrapper


def debug(*args: Any, **kwargs: Any) -> None:
    logger.debug(*args, **kwargs)


def info(*args: Any, **kwargs: Any) -> None:
    logger.info(*args, **kwargs)


def trace(*args: Any, **kwargs: Any) -> None:
    logger.trace(*args, **kwargs)


def success(*args: Any, **kwargs: Any) -> None:
    logger.success(*args, **kwargs)


def warning(*args: Any, **kwargs: Any) -> None:
    logger.warning(*args, **kwargs)


def error(*args: Any, **kwargs: Any) -> None:
    logger.error(*args, **kwargs)


def exception(*args: Any, **kwargs: Any) -> None:
    logger.exception(*args, **kwargs)


__all__ = ["debug", "error", "exception", "info", "property_logger", "success", "trace", "warning"]
