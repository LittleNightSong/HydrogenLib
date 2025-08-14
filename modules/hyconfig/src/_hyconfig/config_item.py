from _hycore.utils import InstanceMapping
from .base import AnnoationSupportContainerBase, update_fields_attrs, get_model
from .config_builtins import Model


class ConfigItemMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.__mapping = InstanceMapping()
        cls.__name = name

    def __get__(cls, instance, owner):
        if instance is None:
            return cls

        if instance not in cls.__mapping:
            cls.__mapping[instance] = cls(cls.__name, instance, owner)

        obj = cls.__mapping[instance]

        if fnc := getattr(obj, '__config_get__', None):
            return fnc()

        return obj


class Middle(AnnoationSupportContainerBase, metaclass=ConfigItemMeta):
    def __config_get__(self):
        return self


class Inline(Middle):
    def __init__(self, name, instance, owner):
        super().__init__()
        update_fields_attrs(
            self, attrs={
                'model': get_model(instance)
            }
        )
        self.__post_init__()

    def __post_init__(self): ...


class Group(Middle):
    __model_type__ = Model

    def __init__(self, name, instance, owner):
        self.__name = name
        self.__model = self.__model_type__()
        self.__parent_model = get_model(instance)
        self.__parent_model.set(self.__name, self.__model)

        update_fields_attrs(
            self, attrs={
                'model': self.__model
            }
        )

        self.__post_init__()

    def __post_init__(self): ...
