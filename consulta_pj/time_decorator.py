import logging
import time
from functools import wraps
from typing import Awaitable, Callable, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


def time_async(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
    @wraps(func)
    async def decorated(*args: P.args, **kwargs: P.kwargs) -> T:
        logging.info(f"{func.__name__}.time.start")
        start = time.time()
        result = await func(*args, **kwargs)
        logging.info(f"{func.__name__}.time.end: {time.time() - start}")
        return result

    return decorated
