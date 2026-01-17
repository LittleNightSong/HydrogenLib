from __future__ import annotations

import asyncio
import socket
from collections.abc import Buffer
from typing import Any, Union, IO

from . import socket_consts


class asyncsocketio:
    def __init__(self, s: Union[asyncsocket, Any] = None):
        self._sock = s or asyncsocket()

    async def write(self, data):
        return await self._sock.sendall(data)

    async def read(self, size: int = -1):
        return await self._sock.recv(size)

    def close(self, closefd=True):
        if not closefd:  # 如果仅仅只是关闭文件描述符，则不关闭socket
            self._sock.close()


type _OptionsType = socket_consts.SocketOptions | socket_consts.IPv6Options | socket_consts.IPOptions | socket_consts.TCPOptions


class _Options:
    def __init__(self, sock):
        self._sock = sock

    def __getitem__(
            self, item: _OptionsType | tuple[_OptionsType, int]
    ):
        opt = item
        buflen = None

        if isinstance(item, tuple):
            opt, buflen = item

        level = opt.__level__
        return self._sock.getsockopt(level.value(), item.value(), buflen)

    def __setitem__(self, key, value):
        opt = key
        level = opt.__level__

        self._sock.setsockopt(
            level.value(), opt.value(), value
        )


class asyncsocket:
    """
    socket.socket的异步包装版本
    """

    def __init__(self, s: Union[socket.socket, 'asyncsocket'] = None, loop: asyncio.AbstractEventLoop = None):
        self.loop = None

        if s is None:
            self.sock = socket.socket()

        elif isinstance(s, asyncsocket):
            self.sock = s.sock
            self.loop = s.loop
        elif isinstance(s, socket.socket):
            self.sock = s
        else:
            raise TypeError('s must be Asyncsocket, socket.socket or None')

        if self.sock.getblocking():
            self.sock.setblocking(False)  # 异步IO采用非阻塞

        self.loop = self.loop or loop or asyncio.get_running_loop()

    async def sendall(self, data):
        return await self.loop.sock_sendall(
            self.sock, data
        )

    async def sendto(self, data, target):
        return await self.loop.sock_sendto(self.sock, data, target)

    async def recv(self, size: int):
        return await self.loop.sock_recv(
            self.sock, size
        )

    async def recv_into(self, buffer):
        return await self.loop.sock_recv_into(
            self.sock, buffer
        )

    async def recvfrom(self, bufsize: int):
        return await self.loop.sock_recvfrom(self.sock, bufsize)

    async def recvfrom_into(self, buf: Buffer, n: int):
        return await self.loop.sock_recvfrom_into(self.sock, buf, n)

    async def sendfile(self, file: IO[bytes], offset: int = 0, count: int = 0, *, fallback=None):
        return await self.loop.sock_sendfile(self.sock, file, offset, count, fallback=fallback)

    async def accept(self):
        conn, addr = await self.loop.sock_accept(self.sock)
        return asyncsocket(conn), addr

    async def connect(self, addr: str, port: int):
        await self.loop.sock_connect(self.sock, (addr, port))
        return self

    @property
    def inheriteable(self):
        return self.sock.get_inheritable()

    @inheriteable.setter
    def inheriteable(self, inheriteable):
        self.sock.set_inheritable(inheriteable)

    def makefile(self) -> asyncsocketio:
        return asyncsocketio(self)

    def listen(self, backlog: int = ...):
        self.sock.listen(backlog)

    @property
    def detach(self):
        return self.sock.detach()

    @property
    def family(self):
        return self.sock.family

    @property
    def fileno(self):
        return self.sock.fileno()

    @property
    def blocking(self):
        return self.sock.getblocking()

    @blocking.setter
    def blocking(self, blocking):
        self.sock.setblocking(blocking)

    @property
    def peer_name(self):
        return self.sock.getpeername()

    @property
    def sock_name(self):
        return self.sock.getsockname()

    def getsockopt(self, level, optname, buflen=None):
        try:
            if buflen is None:
                return self.sock.getsockopt(level, optname)
            else:
                return self.sock.getsockopt(level, optname, buflen)
        except OSError:
            return None

    def setsockopt(self, level, optname, value):
        self.sock.setsockopt(level, optname, value)

    @property
    def timeout(self):
        return self.sock.gettimeout()

    @timeout.setter
    def timeout(self, timeout):
        self.sock.settimeout(timeout)

    @property
    def options(self):
        return _Options(self)

    def ioctl(self, control, option):
        return self.sock.ioctl(control, option)

    def bind(self, addr):
        self.sock.bind(addr)

    def close(self):
        self.sock.close()

    def __del__(self):
        self.sock.close()

    def __enter__(self):
        return self.sock.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.sock.__exit__(exc_type, exc_val, exc_tb)


class asyncudpsocket(asyncsocket):
    target: str

    async def send(self, data):
        return await super().sendto(data, self.target)

    async def recv(self, size: int):
        return await self.recvfrom(size)
