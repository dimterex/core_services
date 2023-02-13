from typing import Awaitable

from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from modules.core.http_server.base_executor import BaseExecutor
from modules.core.rabbitmq.messages.configuration.periodical_task_model import PeriodicalTaskModel
from modules.core.rabbitmq.messages.configuration.periodical_tasks.set_periodical_tasks_request import \
    SetPeriodicalTasksRequest
from modules.core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from modules.core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.configuration.set_base_reponse import SetBaseResponse


class SetPeriodicalTasksRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        tasks: list[PeriodicalTaskModel] = []
        body = await request.json()
        for b in body:
            tasks.append(PeriodicalTaskModel.deserialize(b))

        response = self.rpcPublisher.call(CONFIGURATION_QUEUE, SetPeriodicalTasksRequest(tasks))
        result = SetBaseResponse(response.status)
        if result.status == SUCCESS_STATUS_CODE:
            result.exception = 'Success updated'
        else:
            result.exception = response.message
        return BaseExecutor.generate_response(result)
