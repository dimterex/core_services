import datetime

from jira_tracker.main import JIRA_QUEUE
from modules.core.http_server.web_socket import WebSocketService
from modules.core.rabbitmq.messages.identificators import PROMISE_ID_PROPERTY, MESSAGE_PAYLOAD
from modules.core.rabbitmq.messages.jira_tracker.get_worklogs_request import GetWorklogsRequest
from modules.core.rabbitmq.messages.jira_tracker.get_worklogs_response import GET_WORKLOGS_RESPONSE_WORKLOGS
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.ws_get_worklogs_response import WsGetWorklogsResponse

GET_WORKLOGS_REQUEST_YEAR = 'year'
GET_WORKLOGS_REQUEST_MONTH = 'month'


class WebSocketGetWorklogRequestHandler:
    def __init__(self, ws: WebSocketService, publisher: RpcPublisher):
        self.ws = ws
        self.publisher = publisher

    def execute(self, message):
        promise_id = message[PROMISE_ID_PROPERTY]
        year = message[GET_WORKLOGS_REQUEST_YEAR]
        month = message[GET_WORKLOGS_REQUEST_MONTH]
        request = GetWorklogsRequest(year, month).to_json()
        response = self.publisher.call(JIRA_QUEUE, request)
        worklogs = response[MESSAGE_PAYLOAD][GET_WORKLOGS_RESPONSE_WORKLOGS]
        result = []
        for meeting in worklogs:
            meeting_start_time = meeting.start.replace(hour=meeting.start.hour + 7)
            meeting_end_time = meeting.end.replace(hour=meeting.end.hour + 7)
            message: list[str] = [
                f'Name: {meeting.name}'
                f'\n\tDate: {meeting_start_time.day}-{meeting_start_time.month}-{meeting_start_time.year}'
                f'\n\tTime: {meeting_start_time.hour}:{meeting_start_time.minute}-{meeting_end_time.hour}:{meeting_end_time.minute}'
                f'\n\tLocation: {meeting.location}'
                f'\n\tContent: {meeting.description}'
            ]
            result.append('\n'.join(message))

        ws_response = WsGetWorklogsResponse(result)
        self.ws.send_message(promise_id, ws_response.to_json())

