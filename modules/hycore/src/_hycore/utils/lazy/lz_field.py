import typing
from typing import Callable, Any

from .lz_data import LazyData
from ...better_descriptor import (Descriptor, DescriptorInstance)


class LazyPropertyData[T](DescriptorInstance):
    _lazydata = None

    def __dspt_init__(self, inst, owner, name, dspt: 'LazyProperty'):
        self._lazydata = LazyData(dspt.loader(), inst)

    def __dspt_get__(self, instance, owner, parent: 'LazyProperty') -> T:
        self._lazydata.update_callable(parent.loader())
        return self._lazydata.get(instance)  # 传递实例


class LazyProperty[T](Descriptor):
    def __init__(self, loader: Callable[[Any], T] = None):
        super().__init__()
        self._loader = loader

    def loader(self, loader: Callable[[Any], T] = None):
        if loader:
            self._loader = loader
            return self
        else:
            return self._loader

    def __dspt_new__(self, inst) -> DescriptorInstance:
        return LazyPropertyData()

    if typing.TYPE_CHECKING:
        def __get__(self, inst, owner) -> T: ...
        def __set__(self, inst, value: T): ...


def lazy_property[T](loader: Callable[[Any], T] = None) -> LazyProperty[T]:
    return LazyProperty[T](loader)
