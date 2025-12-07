from __future__ import annotations

import typing
from abc import ABC, abstractmethod

from typing import AsyncContextManager

if typing.TYPE_CHECKING:
    from .response import AbstractResponse


class AbstractSession(ABC):
    @abstractmethod
    async def request(self, method, url, **kwargs) -> AsyncContextManager[AbstractResponse]:
        pass

    @abstractmethod
    async def aclose(self):
        pass




