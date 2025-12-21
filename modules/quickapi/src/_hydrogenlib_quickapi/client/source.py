from __future__ import annotations

from _hydrogenlib_core.descriptor import Descriptor, DescriptorInstance
from .models import AbstractSession
from .models.request import *


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

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = Url(base_url)
