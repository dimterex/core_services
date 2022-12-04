import datetime

from jira_tracker.main import JIRA_QUEUE
from modules.core.http_server.http_request import Http_Request
from modules.core.http_server.http_response import Http_Response
from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD
from modules.core.rabbitmq.messages.jira_tracker.get_worklogs_request import GetWorklogsRequest
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.messages.ws_get_worklogs_response import GET_WORKLOGS_RESPONSE_WORKLOGS


class GetMonthTimeRequestExecutor:
    def __init__(self, rpcPublisher: RpcPublisher):
        self.rpcPublisher = rpcPublisher

    def generate(self, req: Http_Request) -> Http_Response:
        start = datetime.datetime.now()
        print(f'start time = {start}')
        month = int(req.query["month"][0])
        year = int(req.query["year"][0])
        request = GetWorklogsRequest(year, month).to_json()

        response = self.rpcPublisher.call(JIRA_QUEUE, request)
        rawBody = response[MESSAGE_PAYLOAD][GET_WORKLOGS_RESPONSE_WORKLOGS]
        body = f'{rawBody}'.encode('utf-8')

        end = datetime.datetime.now()
        print(f'start time = {end}')
        print(f'diff = {end - start}')

        contentType = 'text/html; charset=utf-8'
        headers = [
            ('Content-Type', contentType),
            ('Content-Length', len(body)),
            ('Access-Control-Allow-Origin', '*'),
        ]
        return Http_Response(200, 'Ok', headers=headers, body=body)

