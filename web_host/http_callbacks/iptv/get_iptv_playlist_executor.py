from typing import Awaitable

from aiohttp import web
from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from core.http_server.base_executor import BaseExecutor
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher


class GetIptvPlaylistExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher, playlist_path: str):
        self.playlist_path = playlist_path
        self.rpcPublisher = rpcPublisher
        self.next_request_time = None

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        return web.FileResponse(self.playlist_path)
