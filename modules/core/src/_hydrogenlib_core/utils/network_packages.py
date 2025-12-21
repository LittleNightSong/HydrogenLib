from abc import abstractmethod

from .auto import AutoState, AutoStr


class NetPackage(AutoState, AutoStr):
    """
    使用时，子类的`_state_attrs` 和 `_str_attrs` 应显式指定，否则可能无法正常序列化
    """
    @abstractmethod
    def get(self): ...

    @classmethod
    def is_package(cls, package_object):
        return isinstance(package_object, cls) or issubclass(package_object.__class__, cls)


class Request(NetPackage):
    __state_attrs__ = ("header", "data")

    def __init__(self, header=None, data=None):
        self.header = {} if header is None else header
        self.data = data

    def get(self):
        return self.header, self.data


class Answer(NetPackage):
    __state_attrs__ = ("header", "result", "status")

    def __init__(self, header=None, result=None, status=None):
        self.header = header
        self.result = result
        self.status = status

    def get(self):
        return self.header, self.result, self.status


class Error(NetPackage):
    __state_attrs__ = ("header", "error", "reason")

    def __init__(self, header=None, error=None, reason=None):
        self.header = header
        self.error = error
        self.reason = reason

    def get(self):
        return self.header, self.error, self.reason


class Info(NetPackage):
    __state_attrs__ = ("header", "info")

    def __init__(self, header=None, info=None):
        self.header = header
        self.info = info

    def get(self):
        return self.header, self.info


class Action(NetPackage):
    __state_attrs__ = ("header", "action")

    def __init__(self, header=None, action=None):
        self.header = header
        self.action = action

    def get(self):
        return self.header, self.action
