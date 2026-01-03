from ..instance_mapping import InstanceMapping
from ...typefunc import alias


class lazy_property[T]:
    fget = alias['_fget']
    fset = alias['_fset']
    fdel = alias['_fdel']

    def __init__(self, fget=None, fset=None, fdel=None):
        self._fget = fget
        self._fset = fset
        self._fdel = fdel
        self._values = InstanceMapping()

    def setter(self, fset):
        self._fset = fset

    def getter(self, fget):
        self._fget = fget

    def deleter(self, fdel):
        self._fdel = fdel

    def __get__(self, instance, owner) -> T:
        if instance in self._values:
            return self._values[instance]
        elif self._fget:
            self._values[instance] = self._fget(instance)
            return self._values[instance]
        else:
            raise AttributeError(f"'{instance.__class__.__name__}' object has no attribute '{self.__name__}'")

    def __set__(self, instance, value):
        if instance in self._values:
            del self._values[instance]

        self._fset(instance, value)

    def __delete__(self, instance):
        if instance in self._values:
            del self._values[instance]

        self._fdel(instance)

