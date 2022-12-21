from typing import Awaitable

from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from modules.core.http_server.base_executor import BaseExecutor
from modules.core.rabbitmq.messages.configuration.category_model import CategoryModel
from modules.core.rabbitmq.messages.configuration.todoits_categories.set_todoits_categories_request import \
    SetTodoistCategoriesRequest
from modules.core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from modules.core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.configuration.set_base_reponse import SetBaseResponse


class SetTodoistCategoryRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        categories: list[CategoryModel] = []
        body = await request.json()

        for b in body:
            categories.append(CategoryModel.deserialize(b))

        response = self.rpcPublisher.call(CONFIGURATION_QUEUE, SetTodoistCategoriesRequest(categories))
        result = SetBaseResponse(response.status)
        if result.status == SUCCESS_STATUS_CODE:
            result.exception = 'Success updated'
        else:
            result.exception = response.message
        return BaseExecutor.generate_response(result)
