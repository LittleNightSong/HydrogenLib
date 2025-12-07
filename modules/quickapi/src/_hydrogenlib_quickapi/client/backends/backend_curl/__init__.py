from typing import AsyncGenerator

from asyncstdlib.itertools import chain, batched

from ...models import *

import curl_cffi


class CurlResponse(AbstractResponse):
    def __init__(self, original_response: curl_cffi.Response):
        self._o = original_response  # Original Response

    @property
    async def content(self) -> bytes:
        return await self._o.acontent()

    @property
    async def text(self) -> str:
        return await self._o.atext()

    @property
    async def json(self):
        return self._o.json()

    @property
    def status_code(self) -> int:
        return self._o.status_code

    async def aclose(self) -> None:
        await self._o.aclose()

    @property
    def stream_reader(self) -> 'CurlStreamReader':
        return CurlStreamReader(self._o)


class CurlStreamReader(AbstractStreamReader):
    def __init__(self, original_response: curl_cffi.Response):
        self._o = original_response  # Original Response
        self._reader = None

    async def _dynamic_reader(self):
        buffer = b''
        chunked_data = self._o.aiter_content()

        length = yield b''
        while length:
            while len(buffer) < length:
                buffer += await chunked_data.anext()


    async def _dynamic_reader_start(self):
        if not self._reader:
            self._reader = self._dynamic_reader()
            await self._reader.asend(None)

    async def _dynamic_read(self, n=-1):
        if n == -1:
            return await self._o.acontent()
        else:  # 向 dynamic_reader 获取数据
            return await self._reader.asend(n)

    async def iter_chunks(self, chunk_size: int = None) -> AsyncGenerator[bytes]:
        ...
    async def iter_chunks_exactly(self, chunk_size: int = None) -> AsyncGenerator[bytes]:
        async for i in batched(chain.from_iterable(self.iter_chunks(chunk_size)), chunk_size):
            yield b''.join(i)

    async def read(self, n=-1):
        if n == -1:
            return await self._o.acontent()
        else:
            return await self._o

    async def close(self) -> None:
        pass

    async def read_exactly(self, n: int) -> bytes:
        pass
