from ..models import *
from .. import function as _apifnc


class _api:
    def function(self, path, method='GET'):
        def decorator(func):
            return _apifnc.ApiFunction(func, method, path)

        return decorator

    def get(self, path):
        return self.function(path, 'GET')

    def post(self, path):
        return self.function(path, 'POST')

    def put(self, path):
        return self.function(path, 'PUT')

    def delete(self, path):
        return self.function(path, 'DELETE')


def fill_path(method: Literal['template', 'format', 'path'] = 'format', *args, **kwds) -> Request:
    req = Request(
        None, UrlPath('', method, *args, **kwds)
    )

    return req


def set_stream(method: RequestMethod, stream: AsyncGenerator, **kwds):
    req = Request(
        None, UrlPath('', 'path'), method=method, body=stream, **kwds
    )
    return req


def check_status(response, cases):
    status = response.status_code

    for case in cases:
        if isinstance(case, range) and status in case or status == case:
            raise RuntimeError(f'{case}: {cases.get(case)}')


api = _api()
