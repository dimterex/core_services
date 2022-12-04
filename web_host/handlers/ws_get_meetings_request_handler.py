import datetime

from modules.core.helpers.helper import convert_rawdate_to_datetime
from modules.core.http_server.web_socket import WebSocketService
from modules.core.rabbitmq.messages.identificators import PROMISE_ID_PROPERTY, MESSAGE_PAYLOAD
from modules.core.rabbitmq.messages.outlook.get_events_by_date_request import GetEventsByDateRequest
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from outlook.main import OUTLOOK_QUEUE
from web_host.messages.ws_get_events_response import Ws_Get_Events_Response


class WsGetMeetingsRequestHandler:
    def __init__(self, ws: WebSocketService, publisher: RpcPublisher):
        self.ws = ws
        self.publisher = publisher

    def execute(self, message):
        promise_id = message[PROMISE_ID_PROPERTY]
        start_time = convert_rawdate_to_datetime(message['date'])
        start_time = start_time.replace(tzinfo=datetime.timezone.utc)
        request = GetEventsByDateRequest(start_time).to_json()
        response = self.publisher.call(OUTLOOK_QUEUE, request)
        worklogs: str = response[MESSAGE_PAYLOAD]['events']
        ws_response = Ws_Get_Events_Response(worklogs)
        self.ws.send_message(promise_id, ws_response.to_json())


