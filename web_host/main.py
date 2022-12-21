import os
import warnings

from modules.core.http_server.core_http_server import AiohttpHttpServer
from modules.core.http_server.http_method import HTTPMethod
from modules.core.http_server.http_route import HttpRoute
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.http_callbacks.configuration.get_credentials_request_executor import GetCredentialsRequestExecutor
from web_host.http_callbacks.configuration.get_periodical_tasks_request_executor import \
    GetPeriodicalTasksRequestExecutor
from web_host.http_callbacks.configuration.get_todoist_category_request_executor import \
    GetTodoistCategoryRequestExecutor
from web_host.http_callbacks.configuration.get_tokens_request_executor import GetTokensRequestExecutor
from web_host.http_callbacks.configuration.get_urls_request_executor import GetUrlsRequestExecutor
from web_host.http_callbacks.configuration.set_meetings_category_request_executor import \
    SetMeetingsCategoryRequestExecutor
from web_host.http_callbacks.configuration.set_periodical_tasks_request_executor import \
    SetPeriodicalTasksRequestExecutor
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
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    static_folder = os.environ[STATIC_PATH]
    rpc_publisher = RpcPublisher(ampq_url)
    aiohHttpServer = AiohttpHttpServer(6789)

    react_routers = [
        '/',
        '/configuration',
        '/logger'
    ]

    aiohHttpServer.add_static(static_folder, react_routers)
    aiohHttpServer.add_get_handler([
        HttpRoute(HTTPMethod.GET, '/api/get_month_times', GetMonthTimeRequestExecutor(rpc_publisher, CACHE_RESPONSE_PERIOD_SECONDS)),
        HttpRoute(HTTPMethod.GET, '/api/get_day_events', GetDayEventsRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.GET, '/api/get_day_worklogs', GetDayWorklogsRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.GET, '/api/set_worklog_time', SetWorklogTimeRequestExecutor(rpc_publisher)),

        HttpRoute(HTTPMethod.GET, '/api/configuration/get_credentials', GetCredentialsRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, '/api/configuration/set_credentials', SetCredentialsRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.GET, '/api/configuration/get_meeting_categories', GetMeetingsCategoryRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, '/api/configuration/set_meeting_categories', SetMeetingsCategoryRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.GET, '/api/configuration/get_task_categories', GetTodoistCategoryRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, '/api/configuration/set_task_categories', SetTodoistCategoryRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.GET, '/api/configuration/get_tokens', GetTokensRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, '/api/configuration/set_tokens', SetTokensRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.GET, '/api/configuration/get_urls', GetUrlsRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, '/api/configuration/set_urls', SetUrlsRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.GET, '/api/configuration/get_periodical_tasks', GetPeriodicalTasksRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, '/api/configuration/set_periodical_tasks', SetPeriodicalTasksRequestExecutor(rpc_publisher)),
    ])
    aiohHttpServer.serve_forever()


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    main()

