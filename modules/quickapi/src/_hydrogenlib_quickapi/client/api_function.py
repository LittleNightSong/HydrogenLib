import inspect
import typing

from _hydrogenlib_core.utils import lazy_property
from .models.api_info import APIInfo
from .models.request import Request

if typing.TYPE_CHECKING:
    from .source import  Source

class APIFunction:
    def __init__(self, api_info: APIInfo) -> None:
        self.api_info = api_info
        self.source = None

    @lazy_property
    def signature(self):
        return inspect.Signature(
            parameters=self.api_info.needed_arguments
        )

    def __call__(self, *args, **kwargs):
        boundargs = self.signature.bind(*args, **kwargs)
        boundargs.apply_defaults()

        # 构建 Request
        request = Request(
            url=self.source.base_url
        )