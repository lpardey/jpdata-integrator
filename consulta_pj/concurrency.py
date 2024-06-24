import asyncio
import logging
from typing import Awaitable, Iterable, TypeVar

T = TypeVar("T")


async def log_progress(message: str, index: int, total: int, coro: Awaitable[T], level: int = logging.INFO) -> T:
    logging.log(level, f"Task {message}: {index + 1}/{total}")
    return await coro


async def gather_with_concurrency(n: int, coros: Iterable[Awaitable[T]]) -> list[T]:
    semaphore = asyncio.Semaphore(n)

    async def sem_coro(coro: Awaitable[T]) -> T:
        async with semaphore:
            return await coro

    return await asyncio.gather(*(sem_coro(c) for c in coros))
