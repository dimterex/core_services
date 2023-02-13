from typing import Awaitable

from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from modules.core.helpers.helper import convert_rawdate_to_datetime
from modules.core.http_server.base_executor import BaseExecutor
from modules.core.rabbitmq.messages.identificators import WORKLOG_QUEUE
from modules.core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE
from modules.core.rabbitmq.messages.worklog.write_worklog_request import Write_Worklog_Request
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.statistics.set_worklog_response import SetWorklogResponse
from web_host.messages.statistics.write_worklog_request import WriteWorklogsRequest


class SetWorklogTimeRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        body = await request.json()

        writeModel = WriteWorklogsRequest.deserialize(body)

        date_time = convert_rawdate_to_datetime(f'{writeModel.year}/{writeModel.month}/{writeModel.date}')
        write_worklog_request = Write_Worklog_Request(date_time)
        response = self.rpcPublisher.call(WORKLOG_QUEUE, write_worklog_request)

        result = SetWorklogResponse('ok')
        if result.status == SUCCESS_STATUS_CODE:
            result.messages = response.message
        else:
            result.exception = response.message

        return BaseExecutor.generate_response(result)
