from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from typing import Awaitable

from modules.core.http_server.base_executor import BaseExecutor
from modules.core.rabbitmq.messages.identificators import SYNC_APPLICATION_QUEUE
from modules.core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE, StatusResponse
from modules.core.rabbitmq.messages.sync_application.get_history_request import GetSyncHistoryRequest
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.sync.sync_history_response import SyncHistoryResponse


class GetSyncHistoryRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        response: StatusResponse = self.rpcPublisher.call(SYNC_APPLICATION_QUEUE, GetSyncHistoryRequest())
        result = SyncHistoryResponse(response.status, response.message)
        if result.status == SUCCESS_STATUS_CODE:
            result.items = response.message
        else:
            result.exception = response.message

        return BaseExecutor.generate_response(result)
