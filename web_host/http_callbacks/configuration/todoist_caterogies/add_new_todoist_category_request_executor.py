from typing import Awaitable

from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from core.http_server.base_executor import BaseExecutor
from core.rabbitmq.messages.configuration.todoits_categories.add_new_todoist_category_request import \
    AddNewTodoistCategoryRequest
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.configuration.set_base_reponse import SetBaseResponse


class AddNewTodoistCategoryRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        response = self.rpcPublisher.call(CONFIGURATION_QUEUE, AddNewTodoistCategoryRequest())

        result = SetBaseResponse(response.status, response.message)

        return BaseExecutor.generate_response(result)
