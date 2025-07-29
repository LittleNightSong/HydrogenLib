import dataclasses as dc
import json
from string import Template
from typing import Literal, AsyncGenerator, AsyncIterable

from _hycore.typefunc import AsyncIO


type RequestMethod = Literal['GET', 'POST', 'PUT', 'DELETE']


@dc.dataclass
class Request:
    base_url: str | None
    path: 'UrlPath'  # 当 path 为 dict 时, 表示填充路径模版
    query: dict = dc.field(default_factory=dict)  # 请求参数
    method: RequestMethod = 'GET'
    headers: dict[str, str] = dc.field(default_factory=dict)
    body: AsyncIterable = None


@dc.dataclass
class Response:
    url: str
    status_code: int
    headers: dict[str, str]
    content: AsyncIO[bytes]

    @property
    async def json(self):
        data = await self.content.read()
        return json.loads(data)


type UrlPathMethod = Literal['template', 'format', 'path']


class UrlPath:
    path: str | str | Template
    method: UrlPathMethod = 'format'
    
    def __init__(self, path, m: UrlPathMethod = 'format', *args, **kwargs):
        self.path = path
        self.method = m
        self.args, self.kwargs = args, kwargs

    def fill_template(self, mapping=None, **kwds):
        if self.method == 'template' and not isinstance(self.path, Template):
            self.path = Template(self.path)

        mapping = mapping or {}
        return self.path.substitute(mapping, **kwds)
    
    def fill_format(self, *args, **kwargs):
        return self.path.format(*args, **kwargs)

    def fill_path(self):
        return self.path
    
    def fill(self, *args, **kwds):
        match self.method:
            case 'template':
                return self.fill_template(kwds)
            case 'format':
                return self.fill_format(*args, **kwds)
            case 'path':
                return self.fill_path()
            case _:
                raise ValueError('method must be template, format or path')
    
    def __str__(self):
        return self.fill(*self.args, **self.kwargs)
    