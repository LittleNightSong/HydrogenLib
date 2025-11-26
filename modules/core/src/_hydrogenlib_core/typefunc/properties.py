from . import get_attr_by_path as getattr, set_attr_by_path as setattr, del_attr_by_path as delattr
import enum as _enum
from typing import Callable, Any, Self


class aliasmode(int, _enum.Enum):
    read = 0
    write = 1
    read_write = 2


class alias:
    """
    声明属性别名
    """
    mode = aliasmode

    def __init__(self, attr_path, mode=aliasmode.read, classvar_enabled=False):
        self.path = str(attr_path)
        self.mode = mode
        self.cve = classvar_enabled

    def __str__(self):
        return self.path

    def __class_getitem__(cls, item) -> 'alias':
        return cls(item)

    def __getitem__(self, item):
        self.path = self.path.removesuffix('.') + '.' + str(item)
        return self

    def __call__(self, *, mode=None, classvar_enabled=None) -> Self:
        if mode is not None:
            self.mode = mode
        if classvar_enabled is not None:
            self.cve = classvar_enabled

        return self

    def __get__(self, instance, owner):
        if instance is None:
            if self.cve:
                instance = owner
            else:
                return self
        if self.mode in {aliasmode.read_write, aliasmode.read}:
            return getattr(instance, self.path)
        raise PermissionError("Can't read alias")

    def __set__(self, instance, value):
        if self.mode in {aliasmode.read_write, aliasmode.write}:
            setattr(instance, self.path, value)
            return
        raise PermissionError("Can't write alias")

    def __delete__(self, instance):
        if self.mode in {aliasmode.read_write, aliasmode.write}:
            delattr(instance, self.path)
        raise PermissionError("Can't delete alias")


class rolling_back:
    """
    回滚属性

    当访问的属性为 None 或发生错误时, 读取属性时将会返回回滚属性的值
    """

    def __init__(self, attr_path, *, rolling_backs: list[str] = None):
        self.path = str(attr_path)
        self.rolling_backs = rolling_backs or []

    def iter_rolling_backs(self):
        for r in self.rolling_backs:
            yield getattr(self, r)

    def __get__(self, instance, owner):
        try:
            value = getattr(instance, self.path)
        except:
            value = None

        while value is None:
            try:
                value = next(self.iter_rolling_backs())
            except:
                pass

        return value

    def __set__(self, instance, value):
        setattr(instance, self.path, value)

    def __delete__(self, instance):
        delattr(instance, self.path)
