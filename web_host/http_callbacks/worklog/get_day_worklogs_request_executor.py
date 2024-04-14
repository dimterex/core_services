from typing import Awaitable

from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from core.helpers.helper import convert_rawdate_to_datetime
from core.http_server.base_executor import BaseExecutor
from core.rabbitmq.messages.identificators import WORKLOG_QUEUE
from core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE, StatusResponse
from core.rabbitmq.messages.worklog.get_history_by_date_request import GetHistoryByDateRequest
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.get_history_item_response import HistoryItemResponse


class GetDayWorklogsRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        month = int(request.query["month"])
        year = int(request.query["year"])
        day = int(request.query["day"])
        date_time = convert_rawdate_to_datetime(f'{year}/{month}/{day}')

        request = GetHistoryByDateRequest(date_time)
        response: StatusResponse = self.rpcPublisher.call(WORKLOG_QUEUE, request)

        result = HistoryItemResponse(response.status)
        if result.status == SUCCESS_STATUS_CODE:
            meetings = response.message
            result.messages = meetings
        else:
            result.exception = response.message

        return BaseExecutor.generate_response(result)
