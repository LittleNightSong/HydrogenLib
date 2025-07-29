from _hycore.typefunc import as_aiter
from ..function import ApiFunction
from ..models import Request, UrlPath, Response


def ModelApiFunction(method, path, req_model, res_model, headers=None):
    async def model_adapter(self, *args, **kwds):
        model = req_model(*args, **kwds)
        return Request(
            '', UrlPath(), method='POST',
            body=as_aiter([model.json()]),
        )

    async def model_handler(self, res: Response):
        return res_model.model_validate_json(await res.content.read())

    return ApiFunction(
        model_adapter, method, path, model_handler, headers
    )
