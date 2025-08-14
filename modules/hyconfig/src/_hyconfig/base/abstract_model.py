from abc import ABC, abstractmethod

from typing_extensions import overload


class AbstractModel(ABC):
    @abstractmethod
    @overload
    def get(self, key): ...

    @abstractmethod
    @overload
    def get(self, key, default): ...

    @abstractmethod
    def get(self, key, default=None): ...

    @abstractmethod
    def set(self, key, value): ...

    @abstractmethod
    def exists(self, key): ...

    @abstractmethod
    def init(self, data): ...

    @abstractmethod
    def as_dict(self) -> dict: ...

    def __getitem__(self, item):
        return self.get(item)

    def __contains__(self, item):
        return self.exists(item)
