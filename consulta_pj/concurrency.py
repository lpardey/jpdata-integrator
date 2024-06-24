import asyncio
import logging
from typing import Coroutine, Iterable, TypeVar

Coro = TypeVar("Coro", bound=Coroutine)


async def log_progress(message: str, index: int, total: int, coro: Coro, level: int = logging.INFO) -> Coro:
    logging.log(level, f"Task {message}: {index + 1}/{total}")
    return await coro


async def gather_with_concurrency(n: int, coros: Iterable[Coroutine]):
    semaphore = asyncio.Semaphore(n)

    async def sem_coro(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(sem_coro(c) for c in coros))
