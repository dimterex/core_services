from typing import Awaitable

from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from core.http_server.base_executor import BaseExecutor
from core.rabbitmq.messages.identificators import JIRA_QUEUE
from core.rabbitmq.messages.jira_tracker.get_statistics_request import GetStatisticsRequest
from core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.statistics.get_month_times_response import MonthTimesResponse


class GetMonthTimeRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher, cash_period_time: int):
        self.cache_period_time = cash_period_time
        self.rpcPublisher = rpcPublisher
        self.next_request_time = None

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        month = int(request.query["month"])
        year = int(request.query["year"])

        request = GetStatisticsRequest(year, month)
        response = self.rpcPublisher.call(JIRA_QUEUE, request)
        result = MonthTimesResponse(response.status)
        if result.status == SUCCESS_STATUS_CODE:
            result.messages = response.message
        else:
            result.exception = response.message

        return BaseExecutor.generate_response(result)
