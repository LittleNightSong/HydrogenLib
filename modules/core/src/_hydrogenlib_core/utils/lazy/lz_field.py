from typing import Callable, Self

from ..instance_dict import InstanceMapping


class lazy_property[T]:
    def __init__(self, loader: Callable[[Self], T] = None):
        super().__init__()
        self._loader = loader
        self._values = InstanceMapping()

    def __get__(self, inst, owner) -> T:
        if inst in self._values:
            return self._values[inst]
        elif self._loader:
            self._values[inst] = self._loader(inst)
            return self._values[inst]
        else:
            raise AttributeError(f"'{inst.__class__.__name__}' object has no attribute '{self.__name__}'")

    def __set__(self, inst, value: T | None):
        if value is None:
            del self._values[inst]
            return

        self._values[inst] = value
