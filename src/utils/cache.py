from collections.abc import Callable
from functools import wraps
from typing import Any

from cachetools import TTLCache
from cachetools.keys import hashkey


class AsyncCache:
    def __init__(self, maxsize: int, ttl: int):
        self.__cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def __call__(self, func: Callable):
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = hashkey(*args, **kwargs)
            if key not in self.__cache:
                result = await func(*args, **kwargs)
                self.__cache[key] = result

            return self.__cache[key]

        return wrapper
