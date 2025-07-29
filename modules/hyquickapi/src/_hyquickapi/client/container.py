from .models import Request, Response


class HttpAPI:
    base_url = ''

    async def request(self, request: Request) -> Response:
        ...
