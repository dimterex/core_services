from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from typing import Awaitable

from modules.core.http_server.base_executor import BaseExecutor
from modules.core.rabbitmq.messages.docker_bot.get_container_with_ports_request import GetContainerWithPortsRequest
from modules.core.rabbitmq.messages.identificators import DOCKER_QUEUE, SYNC_APPLICATION_QUEUE
from modules.core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE, StatusResponse
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.get_container_with_ports_response import GetContainerWithPortsResponse


class GetSyncHistoryRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        response: StatusResponse = self.rpcPublisher.call(SYNC_APPLICATION_QUEUE, GetContainerWithPortsRequest())

        result = GetContainerWithPortsResponse(response.status)

        if result.status == SUCCESS_STATUS_CODE:
            result.messages = response.message
        else:
            result.exception = response.message

        return BaseExecutor.generate_response(result)
