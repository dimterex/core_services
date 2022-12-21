from aiohttp.web_fileresponse import FileResponse
from requests import Response

from modules.core.http_server.base_executor import BaseExecutor

from typing import Awaitable

from aiohttp.abc import Request


class ResourceExecutor(BaseExecutor):
    def __init__(self, file: str):
        self.file = file

    async def execute(self, request: Request) -> Awaitable[Response]:
        print(request.path)
        print(self.file)
        return FileResponse(self.file)
