import datetime
from typing import Awaitable

from aiohttp.abc import Request
from aiohttp.web_response import StreamResponse

from core.helpers.helper import convert_rawdate_to_datetime
from core.http_server.base_executor import BaseExecutor
from core.rabbitmq.messages.identificators import OUTLOOK_QUEUE
from core.rabbitmq.messages.outlook.get_events_by_date_request import GetEventsByDateRequest
from core.rabbitmq.messages.status_response import StatusResponse, SUCCESS_STATUS_CODE
from core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.get_day_events_response import DayEventsResponse


class GetDayEventsRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        month = int(request.query["month"])
        year = int(request.query["year"])
        day = int(request.query["day"])
        date_time = convert_rawdate_to_datetime(f'{year}/{month}/{day}')
        date_time = date_time.replace(tzinfo=datetime.timezone.utc)

        request = GetEventsByDateRequest(date_time)
        response: StatusResponse = self.rpcPublisher.call(OUTLOOK_QUEUE, request)
        result = DayEventsResponse(response.status)

        if result.status == SUCCESS_STATUS_CODE:
            result.messages = response.message
        else:
            result.exception = response.message

        return BaseExecutor.generate_response(result)
