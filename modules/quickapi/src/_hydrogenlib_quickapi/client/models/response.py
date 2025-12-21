from abc import ABC, abstractmethod

from .stream_reader import AbstractStreamReader


class AbstractResponse(ABC):
    @property
    @abstractmethod
    async def content(self) -> bytes: ...

    @property
    @abstractmethod
    async def text(self) -> str: ...

    @property
    @abstractmethod
    async def json(self): ...

    @property
    @abstractmethod
    def status_code(self) -> int: ...

    @abstractmethod
    async def aclose(self) -> None: ...

    @property
    @abstractmethod
    def stream_reader(self) -> AbstractStreamReader: ...
