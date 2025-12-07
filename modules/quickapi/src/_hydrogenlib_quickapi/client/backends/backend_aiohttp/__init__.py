from __future__ import annotations

import contextlib
import typing
# from asyncstdlib.itertools import batched, chain
from typing import AsyncGenerator

from ...models import *

# if typing.TYPE_CHECKING:
import aiohttp
from aiohttp.client import _BaseRequestContextManager


class AiohttpStreamReader(AbstractStreamReader):
    __slots__ = ['_resp']

    def __init__(self, original_response: aiohttp.ClientResponse):
        self._resp = original_response

    async def readany(self) -> bytes:
        return await self._resp.content.readany()

    async def iter_chunks(self, max_chunk_size: int = None) -> AsyncGenerator[bytes]:
        if max_chunk_size is None:
            async for data in self._resp.content.iter_any():
                yield data
        else:
            async for data, _ in self._resp.content.iter_chunked(max_chunk_size):
                yield data

    async def iter_chunks_exactly(self, chunk_size: int = 65535) -> AsyncGenerator[bytes]:
        # chunks = batched(
        #     chain.from_iterable(self.iter_chunks(chunk_size)), chunk_size, True
        # )
        # async for i in chunks:
        #     yield b''.join(i)

        while not self._resp.content.at_eof():
            yield await self._resp.content.readexactly(chunk_size)

    async def read(self, n=-1):
        return await self._resp.content.read(n)

    async def read_exactly(self, n: int) -> bytes:
        return await self._resp.content.readexactly(n)

    def is_eof(self) -> bool:
        return self._resp.content.is_eof()

    def at_eof(self) -> bool:
        return self._resp.content.at_eof()

    async def close(self) -> None:
        self._resp.close()

    def __aiter__(self):
        return self._resp.content.__aiter__()


class AiohttpResponse(AbstractResponse):
    __slots__ = ['_o']

    def __init__(self, original_response: aiohttp.ClientResponse):
        self._o = original_response

    @property
    async def content(self) -> bytes:
        return await self._o.read()

    @property
    async def text(self) -> str:
        return await self._o.text()

    @property
    async def json(self):
        return await self._o.json()

    @property
    def status_code(self) -> int:
        return self._o.status

    async def aclose(self) -> None:
        self._o.close()

    @property
    def stream_reader(self) -> AbstractStreamReader:
        return AiohttpStreamReader(self._o)


class AiohttpSession(AbstractSession):
    __slots__ = ['_s']

    def __init__(self, *args, **kwargs):
        self._s = aiohttp.ClientSession(*args, **kwargs)

    @contextlib.asynccontextmanager
    async def request(self, method, url, **kwargs):
        resp = self._s.request(method, url, **kwargs)
        try:
            yield AiohttpResponse(await resp.__aenter__())
        except Exception as e:
            await resp.__aexit__(type(e), e, e.__traceback__)
        finally:
            resp.close()

    async def aclose(self):
        await self._s.close()

    async def __aenter__(self):
        await self._s.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self._s.__aexit__(exc_type, exc_val, exc_tb)
