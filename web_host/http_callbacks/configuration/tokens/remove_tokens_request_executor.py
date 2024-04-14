from typing import Awaitable

from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from core.http_server.base_executor import BaseExecutor
from core.rabbitmq.messages.configuration.tokens.remove_tokens_request import RemoveTokensRequest
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.configuration.set_base_reponse import SetBaseResponse


class RemoveTokensRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        body = await request.json()
        categories: list[int] = body

        response = self.rpcPublisher.call(CONFIGURATION_QUEUE, RemoveTokensRequest(categories))

        result = SetBaseResponse(response.status)
        if result.status == SUCCESS_STATUS_CODE:
            result.exception = 'Success'
        else:
            result.exception = response.message

        return BaseExecutor.generate_response(result)
