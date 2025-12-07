from __future__ import annotations

import pathlib
import typing
from dataclasses import dataclass
from typing import Literal, Any
from yarl import URL as Url


GET, POST, PUT, DELETE, OPTIONS, HEAD, TRACE, PATCH, QUERY = 'GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD', 'TRACE', 'PATCH', 'QUERY'

HttpMethods = Literal['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD', 'TRACE', 'PATCH', 'QUERY']


@dataclass
class Request:
    url: Url = None
    body: dict | str | bytes | typing.Iterable[bytes] = None
    json: dict = None
    stream: bool = None
    headers: dict = None
    cookies: dict = None
    query: dict = None
    timeout: float = 10
    verify: bool = True
    files: list[str | pathlib.Path] = None
    proxy: str = None
    cert: str | tuple[str, str] = None
    auth: tuple[str, str] = None
    allow_redirects: bool = True
    method: HttpMethods = GET  # Method 应通过 __class_getitem__ 设置, 即 Request[POST](...)

    def __class_getitem__(cls, item: HttpMethods) -> type['Request']:
        def wrapper(*args, **kwargs):
            return Request(*args, **kwargs, method=item)

        return wrapper

