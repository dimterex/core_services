from typing import Awaitable

from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from core.http_server.base_executor import BaseExecutor
from core.rabbitmq.messages.configuration.periodical_tasks.add_new_periodical_task_request import \
    AddNewPeriodicalTaskRequest
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.configuration.set_base_reponse import SetBaseResponse


class AddNewPeriodicalTaskRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        response = self.rpcPublisher.call(CONFIGURATION_QUEUE, AddNewPeriodicalTaskRequest())

        result = SetBaseResponse(response.status, response.message)

        return BaseExecutor.generate_response(result)
