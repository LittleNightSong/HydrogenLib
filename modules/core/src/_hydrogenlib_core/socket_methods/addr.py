from .socket_consts import *


def getaddrinfo(
        host: bytes | str | None,
        port: bytes | str | int | None,
        family: int = AddressFamily.UnSpec,
        type: int = 0,
        proto: int = 0,
        flags: int = 0) -> list[
    tuple[AddressFamily, SocketKind, int, str, tuple[str, int] | tuple[str, int, int, int] | tuple[int, bytes]]
]:
    return socket.getaddrinfo(host, port, family, type, proto, flags)
