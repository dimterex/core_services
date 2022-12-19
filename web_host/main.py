import os
import time
import warnings

from modules.core.http_server.core_http_server import CoreHttpServer
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from modules.core.http_server.resource_executor import ResourceExecutor
from web_host.http_callbacks.configuration.get_credentials_request_executor import GetCredentialsRequestExecutor
from web_host.http_callbacks.configuration.get_todoist_category_request_executor import \
    GetTodoistCategoryRequestExecutor
from web_host.http_callbacks.configuration.get_tokens_request_executor import GetTokensRequestExecutor
from web_host.http_callbacks.configuration.get_urls_request_executor import GetUrlsRequestExecutor
from web_host.http_callbacks.configuration.set_meetings_category_request_executor import \
    SetMeetingsCategoryRequestExecutor
from web_host.http_callbacks.configuration.set_todoist_category_request_executor import \
    SetTodoistCategoryRequestExecutor
from web_host.http_callbacks.configuration.set_tokens_request_executor import SetTokensRequestExecutor
from web_host.http_callbacks.configuration.set_urls_request_executor import SetUrlsRequestExecutor
from web_host.http_callbacks.get_day_events_request_executor import GetDayEventsRequestExecutor
from web_host.http_callbacks.get_day_worklogs_request_executor import GetDayWorklogsRequestExecutor
from web_host.http_callbacks.configuration.get_meetings_category_request_executor import GetMeetingsCategoryRequestExecutor
from web_host.http_callbacks.get_month_time_request_executor import GetMonthTimeRequestExecutor
from web_host.http_callbacks.configuration.set_credentials_request_executor import SetCredentialsRequestExecutor
from web_host.http_callbacks.set_worklog_time_request_executor import SetWorklogTimeRequestExecutor

STATIC_PATH = 'STATIC_PATH'
CACHE_RESPONSE_PERIOD_SECONDS = 1800
RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'


def main():
    logger_service = Logger_Service()
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    static_folder = os.environ[STATIC_PATH]

    rpc_publisher = RpcPublisher(ampq_url)

    httpServer = CoreHttpServer(6789, logger_service)
    main_page = "index.html"
    for dp, dn, filenames in os.walk(static_folder):
        for f in filenames:
            full_path = os.path.join(dp, f)
            html_path = full_path.replace(static_folder, str())
            html_path = html_path.replace('\\', '/')
            if f == main_page:
                httpServer.add_handler('/', ResourceExecutor(full_path))
                httpServer.add_handler('/logger', ResourceExecutor(full_path))
                httpServer.add_handler('/configuration', ResourceExecutor(full_path))
                continue

            httpServer.add_handler(html_path, ResourceExecutor(full_path))

    httpServer.add_handler('/api/get_month_times', GetMonthTimeRequestExecutor(rpc_publisher, CACHE_RESPONSE_PERIOD_SECONDS))
    httpServer.add_handler('/api/get_day_events', GetDayEventsRequestExecutor(rpc_publisher))
    httpServer.add_handler('/api/get_day_worklogs', GetDayWorklogsRequestExecutor(rpc_publisher))
    httpServer.add_handler('/api/set_worklog_time', SetWorklogTimeRequestExecutor(rpc_publisher))


    httpServer.add_handler('/api/configuration/get_credentials', GetCredentialsRequestExecutor(rpc_publisher))
    httpServer.add_handler('/api/configuration/set_credentials', SetCredentialsRequestExecutor(rpc_publisher))
    httpServer.add_handler('/api/configuration/get_meeting_categories', GetMeetingsCategoryRequestExecutor(rpc_publisher))
    httpServer.add_handler('/api/configuration/set_meeting_categories', SetMeetingsCategoryRequestExecutor(rpc_publisher))
    httpServer.add_handler('/api/configuration/get_task_categories', GetTodoistCategoryRequestExecutor(rpc_publisher))
    httpServer.add_handler('/api/configuration/set_task_categories', SetTodoistCategoryRequestExecutor(rpc_publisher))
    httpServer.add_handler('/api/configuration/get_tokens', GetTokensRequestExecutor(rpc_publisher))
    httpServer.add_handler('/api/configuration/set_tokens', SetTokensRequestExecutor(rpc_publisher))
    httpServer.add_handler('/api/configuration/get_urls', GetUrlsRequestExecutor(rpc_publisher))
    httpServer.add_handler('/api/configuration/set_urls', SetUrlsRequestExecutor(rpc_publisher))

    httpServer.serve_forever()
    # hostname = '0.0.0.0'
    # websocket_port = 60009
    # ws = WebSocketService(hostname, websocket_port)
    #
    # ws.configute(GET_WORKLOGS_REQUEST_MESSAGE_TYPE, WebSocketGetWorklogRequestHandler(ws, rpc_publisher))
    # ws.configute(GET_EVENTS_REQUEST_MESSAGE_TYPE, WsGetMeetingsRequestHandler(ws, rpc_publisher))


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

