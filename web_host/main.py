import os
import time
import warnings

from modules.core.http_server.core_http_server import CoreHttpServer
from modules.core.http_server.web_socket import WebSocketService
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.identificators import LOGGER_QUEUE
from modules.core.rabbitmq.publisher import Publisher
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.handlers.ws_get_meetings_request_handler import WsGetMeetingsRequestHandler
from web_host.handlers.ws_get_worklog_request_handler import WebSocketGetWorklogRequestHandler
from modules.core.http_server.resource_executor import ResourceExecutor
from web_host.http_callbacks.get_month_time_request_executor import GetMonthTimeRequestExecutor
from web_host.messages.request_types import GET_WORKLOGS_REQUEST_MESSAGE_TYPE, GET_EVENTS_REQUEST_MESSAGE_TYPE

HOST_ENVIRON = 'RABBIT_HOST'
PORT_ENVIRON = 'RABBIT_PORT'


def main():
    host = os.environ[HOST_ENVIRON]
    raw_port = os.environ[PORT_ENVIRON]
    port = int(raw_port)

    logger_service = Logger_Service('Web_host_application')
    ampq_url = f'amqp://guest:guest@{host}:{port}'
    publisher = Publisher(ampq_url)
    rpc_publisher = RpcPublisher(ampq_url)

    # def send_log(log_message):
    #     publisher.send_message(LOGGER_QUEUE, log_message.to_json())
    #
    # logger_service.configure_action(send_log)

    httpServer = CoreHttpServer(6789, logger_service, host='190.160.1.136')
    static_folder = "D:\\Projects\\outlook2tracker\\web_host\\pages"
    main_page = "index.html"
    for dp, dn, filenames in os.walk(static_folder):
        for f in filenames:
            full_path = os.path.join(dp, f)
            html_path = full_path.replace(static_folder, str())
            html_path = html_path.replace('\\', '/')
            if f == main_page:
                html_path = "/"
            httpServer.add_handler(html_path, ResourceExecutor(full_path))

    httpServer.add_handler('/get_month_times', GetMonthTimeRequestExecutor(rpc_publisher))
    httpServer.serve_forever()
    hostname = '0.0.0.0'
    websocket_port = 60009
    ws = WebSocketService(hostname, websocket_port)

    ws.configute(GET_WORKLOGS_REQUEST_MESSAGE_TYPE, WebSocketGetWorklogRequestHandler(ws, rpc_publisher))
    ws.configute(GET_EVENTS_REQUEST_MESSAGE_TYPE, WsGetMeetingsRequestHandler(ws, rpc_publisher))


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    print('Starting')
    main()
    print('Started')
    try:
        while True:
            time.sleep(1)
    finally:
        pass

