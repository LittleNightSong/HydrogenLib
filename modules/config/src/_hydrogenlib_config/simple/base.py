from typing import MutableMapping, Any

import _hydrogenlib_config_core
from .gtr import gtr


class ConfigBase(_hydrogenlib_config_core.base.ConfigBase, middle=True):
    __config_type_registry__ = 'global'

    def __init_subclass__(cls, *, middle=False, mixins=(), **kwargs):
        if middle:
            return

        if cls.__config_type_registry__ == 'global':
            cls.__config_type_registry__ = gtr.create_sub_registry()  # 创建子注册表，防止污染父类

        super().__init_subclass__()

        for name, field in cls.__config_fields__.items():  # 应用 mixin 设置
            for mixin in mixins:
                mixin_ins = mixin() if isinstance(mixin, type) else mixin
                if mixin_ins.check(field.info):
                    mixin_ins.apply(field.info, cls.__config_type_registry__)
                del mixin_ins

    def as_dict(self, for_serializer=False):
        fields = self.__config_fields__
        return {
            name: fields[name].value(self)
            for name in fields  # 普通的 to_dict 转换
        } if not for_serializer else {
            key: fields[name].value_for_serializer(self)  # 应用自定义序列化逻辑
            for key, name in self.__config_alias__.items()
        }  # 序列化场景下，需要应用别名

    @classmethod
    def load(cls, obj: MutableMapping[str, Any]):
        cfg = cls()
        for k, v in obj.items():
            setattr(cfg, k, v)
        return cfg

    def __repr__(self):
        pairs = ", ".join(
            map(
                lambda x: f'{x}={getattr(self, x)!r}',
                self.__config_fields__
            )
        )
        string = f'{self.__class__.__name__}({pairs})'
        return string

    __str__ = __repr__

    def __setattr__(self, key, value):
        if key in self.__config_fields__:
            super().__setattr__(key, value)
        elif alias := self.__config_alias__.get(key):
            super().__setattr__(alias, value)
        else:
            super().__setattr__(key, value)
