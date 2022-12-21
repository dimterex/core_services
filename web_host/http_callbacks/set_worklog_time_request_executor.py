from typing import Awaitable

from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from modules.core.helpers.helper import convert_rawdate_to_datetime
from modules.core.http_server.base_executor import BaseExecutor
from modules.core.rabbitmq.messages.identificators import WORKLOG_QUEUE
from modules.core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE
from modules.core.rabbitmq.messages.worklog.write_worklog_request import Write_Worklog_Request
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.set_worklog_response import SetWorklogResponse


class SetWorklogTimeRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        month = int(request.query["month"])
        year = int(request.query["year"])
        day = int(request.query["day"])

        date_time = convert_rawdate_to_datetime(f'{year}/{month}/{day}')
        request = Write_Worklog_Request(date_time)
        response = self.rpcPublisher.call(WORKLOG_QUEUE, request)

        result = SetWorklogResponse('ok')
        if result.status == SUCCESS_STATUS_CODE:
            result.messages = response.message
        else:
            result.exception = response.message

        return BaseExecutor.generate_response(result)
