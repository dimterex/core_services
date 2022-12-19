import datetime
import json

from modules.core.helpers.helper import convert_rawdate_to_datetime
from modules.core.http_server.base_executor import BaseExecutor
from modules.core.http_server.http_request import Http_Request
from modules.core.http_server.http_response import Http_Response
from modules.core.rabbitmq.messages.identificators import WORKLOG_QUEUE, MESSAGE_PAYLOAD
from modules.core.rabbitmq.messages.status_response import STATUS_RESPONSE_MESSAGE_PROPERTY, SUCCESS_STATUS_CODE
from modules.core.rabbitmq.messages.worklog.write_worklog_request import Write_Worklog_Request
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.set_worklog_response import SetWorklogResponse


class SetWorklogTimeRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    def generate(self, req: Http_Request) -> Http_Response:
        month = int(req.query["month"][0])
        year = int(req.query["year"][0])
        day = int(req.query["day"][0])

        date_time = convert_rawdate_to_datetime(f'{year}/{month}/{day}')
        request = Write_Worklog_Request(date_time)
        response = self.rpcPublisher.call(WORKLOG_QUEUE, request)

        result = SetWorklogResponse(response.status)
        if result.status == SUCCESS_STATUS_CODE:
            result.messages = response.message
        else:
            result.exception = response.message

        return self.generate_success('application/json; charset=utf-8', result)

