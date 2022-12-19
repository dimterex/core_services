import datetime
import json

from modules.core.helpers.helper import convert_rawdate_to_datetime
from modules.core.http_server.base_executor import BaseExecutor
from modules.core.http_server.http_request import Http_Request
from modules.core.http_server.http_response import Http_Response
from modules.core.rabbitmq.messages.identificators import OUTLOOK_QUEUE
from modules.core.rabbitmq.messages.outlook.get_events_by_date_request import GetEventsByDateRequest
from modules.core.rabbitmq.messages.status_response import StatusResponse, SUCCESS_STATUS_CODE
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.get_day_events_response import DayEventsResponse


class GetDayEventsRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    def generate(self, req: Http_Request) -> Http_Response:
        month = int(req.query["month"][0])
        year = int(req.query["year"][0])
        day = int(req.query["day"][0])
        date_time = convert_rawdate_to_datetime(f'{year}/{month}/{day}')
        date_time = date_time.replace(tzinfo=datetime.timezone.utc)

        request = GetEventsByDateRequest(date_time)
        response: StatusResponse = self.rpcPublisher.call(OUTLOOK_QUEUE, request)
        result = DayEventsResponse(response.status)

        if result.status == SUCCESS_STATUS_CODE:
            result.messages = response.message
        else:
            result.exception = response.message

        contentType = 'application/json; charset=utf-8'
        return self.generate_success(contentType, result)
