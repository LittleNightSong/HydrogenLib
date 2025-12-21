from typing import Iterable, AsyncIterator


async def as_aiter[T](obj: Iterable[T]) -> AsyncIterator[T]:
    for item in obj:
        yield item
