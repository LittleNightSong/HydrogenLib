import typing
from typing import Callable, Any
from ..instance_dict import InstanceMapping


class LazyProperty[T, **P]:
    def __init__(self, loader: Callable[P, T] = None):
        super().__init__()
        self._loader = loader
        self._values = InstanceMapping()

    def __get__(self, inst, owner) -> T:
        try:
            return self._values[inst]
        except KeyError:
            if self._loader:
                self._values[inst] = self._loader(inst)
                return self._values[inst]
            else:
                raise AttributeError(f"'{inst.__class__.__name__}' object has no attribute '{self.__name__}'")

    def __set__(self, inst, value: T):
        self._values[inst] = value


def lazy_property[T, **P](loader: Callable[P, T] = None) -> LazyProperty[T, P]:
    return LazyProperty[T, P](loader)
