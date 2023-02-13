from typing import Awaitable

from aiohttp import web
from aiohttp.abc import Request
from aiohttp.web_response import Response

from web_host.messages.base_response import BaseResponse


class BaseExecutor:
    async def execute(self, request: Request) -> Awaitable[Response]:
        raise Exception('Not implemented')

    @staticmethod
    def generate_response(body: BaseResponse) -> Response:
        return web.json_response(body.serialize())
