from string import Template
from typing import Callable, Any

from _hycore.better_descriptor import Descriptor, DescriptorInstance
from _hycore.typefunc import call_property
from .models import *


class ApiFunction(Descriptor):
    _handler = None

    @call_property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, handler: Callable[[Any, Response], Response]):
        if not callable(handler):
            raise TypeError('handler must be callable')
        self._handler = handler

    def __init__(
            self, func, method, path, handler: Callable[[Any, Response], Any] = None, headers: dict[str, str] = None
    ):
        super().__init__()
        self.path = path
        self.method = method
        self.func = func
        self._handler = handler
        self.headers = headers or {}

    def __dspt_new__(self, inst) -> DescriptorInstance:
        return ApiFunctionCallable()


class ApiFunctionCallable(DescriptorInstance):
    def __getattr__(self, item):
        return getattr(
            self._parent, item,
            getattr(self._owner, item, None)
        )

    def __dspt_init__(self, inst, owner, name, dspt):
        self._parent = dspt
        self._inst = inst
        self._owner = owner

    async def __call__(self, *args, **kwargs):
        # 调用用户方法, 获取 Request
        req = await self.func(self._inst, *args, **kwargs)
        if not isinstance(req, Request):
            raise TypeError('func must return Request')

        # 填充 path
        req.path.path = req.path.path or self.path

        # 补充 base_url
        if req.base_url is None:
            req.base_url = self.base_url

        if req.method is None:
            req.method = self.method

        # 现在我们获得了一个完整的 Request
        # 发送请求

        res = await self.request(req)

        if handler := self.handler():
            res = await handler(self._inst, res)

        return res
