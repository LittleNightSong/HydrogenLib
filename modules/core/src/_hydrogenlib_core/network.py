import dataclasses
import socket
from ipaddress import IPv4Address, IPv6Address, AddressValueError
from typing import NamedTuple

import ping3


def IPAddress(value):
    try:
        return IPv4Address(value)
    except AddressValueError:
        return IPv6Address(value)


@dataclasses.dataclass
class HostInfo:
    name: str
    alias: list[str]
    ips: list[IPv4Address | IPv6Address]


ip_class_range = {
    'A': (IPv4Address("10.0.0.0"), IPv4Address("10.255.255.255")),
    'B': (IPv4Address("172.16.0.0"), IPv4Address("172.31.255.255")),
    'C': (IPv4Address("192.168.0.0"), IPv4Address("192.168.255.255")),
    'D': (IPv4Address("110.0.0.0"), IPv4Address("127.255.255.255")),
    'E': (IPv4Address("127.0.0.0"), IPv4Address("127.255.255.255")),
    'F': (IPv4Address("169.254.0.0"), IPv4Address("169.254.255.255")),
}


def ping(name, timeout=1):
    """
    检查网络连通性
    :param name:
    :param timeout:
    :return:
    """
    return ping3.ping(name, timeout=timeout)


def _iter_ip_range(start: IPv4Address | IPv6Address, end: IPv4Address | IPv6Address):
    address_type = type(start)
    if address_type != type(end):
        raise ValueError("start and end must be of the same type")

    for ip in range(int(start), int(end) + 1):
        yield address_type(ip)


def iter_ip_class_range(ip_class: str):
    """
    IP范围：

    - ``A``: ``10.0.0.0``-``10.255.255.255``

    - ``B``: ``172.16.0.0``-``172.31.255.255``

    - ``C``: ``192.168.0.0``-``192.168.255.255``

    - ``D``: ``110.0.0.0``-``127.255.255.255``

    - ``E``: ``127.0.0.0``-``127.255.255.255``

    - ``F``: ``169.254.0.0``-``169.254.255.255``

    :param ip_class: A, B, C, D, E, F
    :return:
    """

    return _iter_ip_range(*ip_class_range[ip_class])


def host_to_ip(host):
    return IPAddress(socket.gethostbyname(host))


def ip_to_host(ip):
    # 尝试将IP地址解析为域名
    name, alias, ips = socket.gethostbyaddr(ip)
    return HostInfo(
        name, alias,
        [IPAddress(ip) for ip in ips]
    )


RemoteAddr = NamedTuple('RemoteAddr', [
    ('host', str),
    ('port', int | None)
])


def parse_remote_addr(remote_addr: str):
    if ':' in remote_addr:
        host, port = remote_addr.split(':')
        port = int(port)

    else:
        host, port = remote_addr, None

    return RemoteAddr(host, port)
