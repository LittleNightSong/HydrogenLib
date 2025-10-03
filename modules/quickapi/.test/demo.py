from _hydrogenlib_quickapi.client import *
from typing import *


class Request:
    ...

class Response:
    ...


class Source:
    def __init__(self, url): ...
    def function(self, path):
        def decorator[**P, T](func: Callable[P, AsyncGenerator[Request, Response]]) -> Callable[[P], T]:
            ...

        return decorator


class MyAPI:
    source = Source('https://xxxxx//api/v1')

    @source.function(path='/list')
    async def list(self, page: int = 0):




