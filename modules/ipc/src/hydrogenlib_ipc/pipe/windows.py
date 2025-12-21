import asyncio

import anyio.lowlevel
import win32event
from win32file import INVALID_HANDLE_VALUE

import win32pipe, win32con, pywintypes


class WinPipeConnectPool:
    def __init__(self, loop=None):
        self._loop = loop or asyncio.get_event_loop()  # type: asyncio.ProactorEventLoop

    async def create(self, name: str, in_buffer_size=1024, out_buffer_size=1024, max_instances=0):
        return await self._loop.create_pipe_connection()
