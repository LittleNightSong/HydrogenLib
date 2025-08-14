from abc import ABC, abstractmethod
import typing


class AbstractBackend(ABC):
    @abstractmethod
    def load(self, fp: typing.IO) -> typing.Any:
        ...

    @abstractmethod
    def dump(self, fp: typing.IO, obj: typing.Any) -> None:
        ...
