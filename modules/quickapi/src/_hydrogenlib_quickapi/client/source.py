from __future__ import annotations

import dataclasses
import inspect
from types import FunctionType
from typing import *

from _hydrogenlib_core.descriptor import Descriptor, DescriptorInstance
from _hydrogenlib_core.typefunc import alias
from _hydrogenlib_core.utils import lazy_property
from . import marks
from .models import AbstractResponse, AbstractSession
from .models.request import *


class ApiFunction(Descriptor):
    class Instance(DescriptorInstance):
        def __dspt_init__(self, inst, owner, name, dspt: ApiFunction):
            self.parent = dspt

        def __getattr__(self, item):
            return getattr(self.parent, item)

        async def request(self, request: Request, source: Source.Instance):
            return await source.request(
                dataclasses.replace(
                    request,
                    url=request.url.joinpath(self.path)
                )
            )

        async def __call__(self, *args, **kwargs):
            params = self.signature.bind(*args, **kwargs)
            params.apply_defaults()

            missing_params = []
            for k, v in params.items():  # 初步检查
                if isinstance(v, marks.Mark) and v.default is marks.undefined:
                    missing_params.append(k)

    @lazy_property
    def signature(self):
        return inspect.signature(self._func)

    @lazy_property
    def return_type(self):
        return self.signature.return_annotation

    @lazy_property
    def parameters(self):
        return self.signature.parameters

    path = alias['_path']
    source = alias['_source']
    method = alias['_method']

    def __init__(self, func: FunctionType, path: str, method: HttpMethods, source: Source = None):
        super().__init__()
        self._path = Url(path)
        self._source = source
        self._method = method
        self._func = func
        self._request_builder = None
        self._compile()

    def _compile(self):
        code_lines = []

        query_params = []
        body_params = []
        path_params = []
        upload_files = []
        upload_file_list = []

        for param in self.parameters.values():
            default = param.default
            name = param.name

            if not isinstance(default, marks.Mark):
                default = marks.FIELD(default)  # 没有特殊标记的当做普通字段
            field = (name, default)
            match default.type:
                case 'QUERY':
                    query_params.append(field)
                case 'PATH':
                    path_params.append(field)
                case 'FIELD':
                    body_params.append(field)
                case 'UPLOAD_FILE':
                    upload_files.append(field)
                case 'UPLOAD_FILE_LIST':
                    upload_file_list.append(field)
                case _:
                    raise ValueError(f'参数 {name} 的类型 {default.type} 不被支持')

        query_code = \
            f"query = {{ {", ".join(f"{repr(name)}: {name}" for name, _ in query_params)} }}"
        path_code = \
            f"path = [{', '.join(name for name, _ in path_params)}]"
        body_code = \
            f"body = {{ {", ".join(f"{repr(name)}: {name}" for name, _ in body_params)} }}"

        upload_files_code = \
            f"files = [{', '.join(name for name, _ in upload_files)}]"
        for name, _ in upload_file_list:
            # 注意要有一个缩进
            upload_files_code += f"\tfiles.extend({name})\n"
        final_code = \
            f"""
from __future__ import annotations  # 防止 signature 中出现未解析的引用
from yarl import URL as Url

def builder{self.signature}:
    # Query
    {query_code if query_params else "query = None"}
    # Path
    {path_code if path_params else "path = ''"}
    # Body
    {body_code if body_params else "body = None"}
    # Upload Files
    {upload_files_code if upload_files or upload_file_list else "files = None"}
    return Request(
        url=Url("{self.path}" + path),
        method={repr(self.method)},
        json=body,
        files=files,
        query=query
    )
"""
        # DEBUG
        with open('final_code.txt', 'w', encoding='utf-8') as f:
            f.write(final_code)

        globals_ = {}
        exec(final_code, globals_)
        self._request_builder = globals_['builder']


class Source(Descriptor):
    class Instance(DescriptorInstance):
        client: AbstractSession

        def __getattr__(self, item):
            return getattr(self.parent, item)

        def __dspt_init__(self, inst, owner, name, dspt):
            self.parent = dspt
            self.replace_config = None

        async def request(self, request: Request):
            final_url = str(self.base_url.extend_query(request.query))

            if self.replace_config:
                final_url = final_url.replace(**self.replace_config)

            response = await self.client.request(
                request.method,
                final_url,
                headers=request.headers,
                cookies=request.cookies,
                timeout=request.timeout,
                verify=request.verify,
                proxy=request.proxy,
                cert=request.cert,
                auth=request.auth,
                allow_redirects=request.allow_redirects,
                stream=request.stream,
                data=request.body
            )

            return response

    def __init__(self, base_url: str, session: AbstractSession = None):
        super().__init__()
        self.base_url = Url(base_url)
        self.session = session

    def define(self, path: str):
        ...

    def function(self, path: str):
        def decorator(fn: Callable[..., AsyncGenerator[Request, AbstractResponse]]):
            return ApiFunction(fn, path, self)

        return decorator
