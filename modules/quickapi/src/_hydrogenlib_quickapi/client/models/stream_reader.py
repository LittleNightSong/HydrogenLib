import typing
from abc import ABC, abstractmethod
from typing import AsyncGenerator, AsyncIterable


class AbstractStreamReader(ABC, AsyncIterable[bytes]):
    @abstractmethod
    async def iter_chunks(self, chunk_size: int = None) -> AsyncGenerator[bytes]: ...

    @abstractmethod
    async def iter_chunks_exactly(self, chunk_size: int = 65535) -> AsyncGenerator[bytes]: ...

    @abstractmethod
    async def read(self, n=-1) -> bytes: ...

    @abstractmethod
    async def readany(self) -> bytes: ...

    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    async def read_exactly(self, n: int) -> bytes: ...

    @abstractmethod
    def at_eof(self) -> bool: ...

    @abstractmethod
    def is_eof(self) -> bool: ...
