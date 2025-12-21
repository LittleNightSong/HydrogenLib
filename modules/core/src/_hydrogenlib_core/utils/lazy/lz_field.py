from typing import Callable, Self, Any

from ..instance_dict import InstanceMapping


class lazy_property[T]:
    def __init__(self, loader: Callable[[...], T] = None):
        self._loader = loader
        self._values = InstanceMapping[Any, T]()

    def __get__(self, inst, owner) -> T:
        if inst in self._values:
            return self._values[inst]
        elif self._loader:
            self._values[inst] = self._loader(inst)
            return self._values[inst]
        else:
            raise AttributeError(f"'{inst.__class__.__name__}' object has no attribute '{self.__name__}'")

