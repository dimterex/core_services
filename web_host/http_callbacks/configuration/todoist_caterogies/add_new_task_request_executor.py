from typing import Awaitable

from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from core.http_server.base_executor import BaseExecutor
from core.rabbitmq.messages.configuration.todoits_categories.add_new_todoist_task_request import \
    AddNewTodoistTaskRequest
from core.rabbitmq.messages.identificators import TODOIST_QUEUE
from core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.configuration.set_base_reponse import SetBaseResponse


class AddNewTaskRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        issue_id = request.query["issue_id"]
        comment = request.query["comment"]
        response = self.rpcPublisher.call(TODOIST_QUEUE, AddNewTodoistTaskRequest(comment, issue_id))

        result = SetBaseResponse(response.status)
        if result.status == SUCCESS_STATUS_CODE:
            result.exception = 'Success'
        else:
            result.exception = response.message

        return BaseExecutor.generate_response(result)
