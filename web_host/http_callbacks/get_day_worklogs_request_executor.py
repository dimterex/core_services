import json

from modules.core.helpers.helper import convert_rawdate_to_datetime
from modules.core.http_server.base_executor import BaseExecutor
from modules.core.http_server.http_request import Http_Request
from modules.core.http_server.http_response import Http_Response
from modules.core.rabbitmq.messages.identificators import WORKLOG_QUEUE
from modules.core.rabbitmq.messages.status_response import SUCCESS_STATUS_CODE, StatusResponse
from modules.core.rabbitmq.messages.worklog.get_history_by_date_request import GetHistoryByDateRequest
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.get_history_item_response import HistoryItemResponse


class GetDayWorklogsRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    def generate(self, req: Http_Request) -> Http_Response:
        month = int(req.query["month"][0])
        year = int(req.query["year"][0])
        day = int(req.query["day"][0])
        date_time = convert_rawdate_to_datetime(f'{year}/{month}/{day}')

        request = GetHistoryByDateRequest(date_time).to_json()
        response: StatusResponse = self.rpcPublisher.call(WORKLOG_QUEUE, request)

        result = HistoryItemResponse(response.status)
        if result.status == SUCCESS_STATUS_CODE:
            meetings = response.message
            result.messages = meetings
        else:
            result.exception = response.message

        return self.generate_success('application/json; charset=utf-8', result)
