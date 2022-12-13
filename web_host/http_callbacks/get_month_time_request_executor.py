import datetime

from jira_tracker.main import JIRA_QUEUE
from modules.core.http_server.base_executor import BaseExecutor
from modules.core.http_server.http_request import Http_Request
from modules.core.http_server.http_response import Http_Response
from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD
from modules.core.rabbitmq.messages.jira_tracker.get_worklogs_request import GetWorklogsRequest
from modules.core.rabbitmq.messages.status_response import STATUS_RESPONSE_STATUS_PROPERTY, ERROR_STATUS_CODE, \
    StatusResponse, STATUS_RESPONSE_MESSAGE_PROPERTY, SUCCESS_STATUS_CODE
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.get_month_times_response import MonthTimesResponse


class GetMonthTimeRequestExecutor(BaseExecutor):
    def __init__(self, rpcPublisher: RpcPublisher, cash_period_time: int ):
        self.cache_period_time = cash_period_time
        self.rpcPublisher = rpcPublisher
        self.last_request: dict[int, dict[int]] = {}
        self.next_request_time = None

    def generate(self, req: Http_Request) -> Http_Response:
        start = datetime.datetime.now()
        print(f'start time = {start}')

        month = int(req.query["month"][0])
        year = int(req.query["year"][0])
        isForce = req.query["force"][0] == 'true'

        response = self.get_cache(start, year, month, isForce)
        end = datetime.datetime.now()
        print(f'end time = {end}')
        print(f'diff = {end - start}')

        return self.generate_success('application/json; charset=utf-8', response)

    def get_cache(self, request_time: datetime, year: int, month: int, isForce: bool) -> MonthTimesResponse:
        if isForce:
            self.update_cache(year, month)
            self.next_request_time = request_time + datetime.timedelta(seconds=self.cache_period_time)

        else:
            if self.next_request_time is None:
                self.update_cache(year, month)
                self.next_request_time = request_time + datetime.timedelta(seconds=self.cache_period_time)

            if year not in self.last_request:
                self.update_cache(year, month)

            if month not in self.last_request[year]:
                self.update_cache(year, month)

            if request_time > self.next_request_time:
                self.update_cache(year, month)
                self.next_request_time = request_time + datetime.timedelta(seconds=self.cache_period_time)

        return self.last_request[year][month]

    def update_cache(self, year: int, month: int):
        if year not in self.last_request:
            self.last_request[year] = {}

        request = GetWorklogsRequest(year, month).to_json()
        response = self.rpcPublisher.call(JIRA_QUEUE, request)
        result = MonthTimesResponse(response.status)
        if result.status == SUCCESS_STATUS_CODE:
            meetings = response.message
            result.messages = meetings
        else:
            result.exception = response.message

        self.last_request[year][month] = result
