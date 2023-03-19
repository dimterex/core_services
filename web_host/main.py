import os
import warnings

from modules.core.http_server.core_http_server import AiohttpHttpServer
from modules.core.http_server.http_method import HTTPMethod
from modules.core.http_server.http_route import HttpRoute
from modules.core.rabbitmq.rpc.rpc_publisher import RpcPublisher
from web_host.http_callbacks.configuration.get_credentials_request_executor import GetCredentialsRequestExecutor
from web_host.http_callbacks.configuration.periodical_tasks.add_new_periodical_task_request_executor import AddNewPeriodicalTaskRequestExecutor
from web_host.http_callbacks.configuration.periodical_tasks.get_periodical_tasks_request_executor import GetPeriodicalTasksRequestExecutor
from web_host.http_callbacks.configuration.periodical_tasks.remove_periodical_tasks_request_executor import RemovePeriodicalTasksRequestExecutor
from web_host.http_callbacks.configuration.todoist_caterogies.add_new_todoist_category_request_executor import AddNewTodoistCategoryRequestExecutor
from web_host.http_callbacks.configuration.todoist_caterogies.get_todoist_category_request_executor import GetTodoistCategoryRequestExecutor
from web_host.http_callbacks.configuration.tokens.add_new_token_request_executor import AddNewTokenRequestExecutor
from web_host.http_callbacks.configuration.tokens.get_tokens_request_executor import GetTokensRequestExecutor
from web_host.http_callbacks.configuration.urls.add_new_url_request_executor import AddNewUrlRequestExecutor
from web_host.http_callbacks.configuration.urls.get_urls_request_executor import GetUrlsRequestExecutor
from web_host.http_callbacks.configuration.meeting_categories.add_new_meeting_category_request_executor import AddNewMeetingCategoryRequestExecutor
from web_host.http_callbacks.configuration.meeting_categories.remove_meeting_categories_request_executor import RemoveMeetingCategoriesRequestExecutor
from web_host.http_callbacks.configuration.meeting_categories.set_meetings_category_request_executor import SetMeetingsCategoryRequestExecutor
from web_host.http_callbacks.configuration.periodical_tasks.set_periodical_tasks_request_executor import SetPeriodicalTasksRequestExecutor
from web_host.http_callbacks.configuration.todoist_caterogies.remove_todoist_categories_request_executor import RemoveTodoistCategoriesRequestExecutor
from web_host.http_callbacks.configuration.todoist_caterogies.set_todoist_category_request_executor import SetTodoistCategoryRequestExecutor
from web_host.http_callbacks.configuration.tokens.remove_tokens_request_executor import RemoveTokensRequestExecutor
from web_host.http_callbacks.configuration.tokens.set_tokens_request_executor import SetTokensRequestExecutor
from web_host.http_callbacks.configuration.urls.remove_urls_request_executor import RemoveUrlsRequestExecutor
from web_host.http_callbacks.configuration.urls.set_urls_request_executor import SetUrlsRequestExecutor
from web_host.http_callbacks.sync_application.get_sync_history_request_executor import GetSyncHistoryRequestExecutor
from web_host.http_callbacks.worklog.get_day_events_request_executor import GetDayEventsRequestExecutor
from web_host.http_callbacks.worklog.get_day_worklogs_request_executor import GetDayWorklogsRequestExecutor
from web_host.http_callbacks.configuration.meeting_categories.get_meetings_category_request_executor import GetMeetingsCategoryRequestExecutor
from web_host.http_callbacks.worklog.get_month_time_request_executor import GetMonthTimeRequestExecutor
from web_host.http_callbacks.configuration.set_credentials_request_executor import SetCredentialsRequestExecutor
from web_host.http_callbacks.worklog.set_worklog_time_request_executor import SetWorklogTimeRequestExecutor
from web_host.http_callbacks.container.get_container_with_ports_request_executor import GetContainerWithPortsRequestExecutor

STATIC_PATH = 'STATIC_PATH'
CACHE_RESPONSE_PERIOD_SECONDS = 1800
RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'

API_PREFIX = "/api"


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
        HttpRoute(HTTPMethod.GET, f'{API_PREFIX}/get_month_times', GetMonthTimeRequestExecutor(rpc_publisher, CACHE_RESPONSE_PERIOD_SECONDS)),
        HttpRoute(HTTPMethod.GET, f'{API_PREFIX}/get_day_events', GetDayEventsRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.GET, f'{API_PREFIX}/get_day_worklogs', GetDayWorklogsRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/set_worklog_time', SetWorklogTimeRequestExecutor(rpc_publisher)),

        # credentials
        HttpRoute(HTTPMethod.GET, f'{API_PREFIX}/configuration/get_credentials', GetCredentialsRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/set_credentials', SetCredentialsRequestExecutor(rpc_publisher)),

        # outlook
        HttpRoute(HTTPMethod.GET, f'{API_PREFIX}/configuration/get_meeting_categories', GetMeetingsCategoryRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/set_meeting_categories', SetMeetingsCategoryRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/add_new_meeting_category', AddNewMeetingCategoryRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/remove_meeting_categories', RemoveMeetingCategoriesRequestExecutor(rpc_publisher)),

        # todoist
        HttpRoute(HTTPMethod.GET, f'{API_PREFIX}/configuration/get_task_categories', GetTodoistCategoryRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/set_task_categories', SetTodoistCategoryRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/add_new_task_category', AddNewTodoistCategoryRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/remove_task_categories', RemoveTodoistCategoriesRequestExecutor(rpc_publisher)),

        # tokens
        HttpRoute(HTTPMethod.GET, f'{API_PREFIX}/configuration/get_tokens', GetTokensRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/set_tokens', SetTokensRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/add_new_token', AddNewTokenRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/remove_tokens', RemoveTokensRequestExecutor(rpc_publisher)),

        # urls
        HttpRoute(HTTPMethod.GET, f'{API_PREFIX}/configuration/get_urls', GetUrlsRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/set_urls', SetUrlsRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/add_new_url', AddNewUrlRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/remove_urls', RemoveUrlsRequestExecutor(rpc_publisher)),

        # periodical tasks
        HttpRoute(HTTPMethod.GET, f'{API_PREFIX}/configuration/get_periodical_tasks', GetPeriodicalTasksRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/set_periodical_tasks', SetPeriodicalTasksRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/add_new_periodical_task', AddNewPeriodicalTaskRequestExecutor(rpc_publisher)),
        HttpRoute(HTTPMethod.PUT, f'{API_PREFIX}/configuration/remove_periodical_tasks', RemovePeriodicalTasksRequestExecutor(rpc_publisher)),

        # docker
        HttpRoute(HTTPMethod.GET, f'{API_PREFIX}/get_container_with_ports', GetContainerWithPortsRequestExecutor(rpc_publisher)),

        # sync
        HttpRoute(HTTPMethod.GET, f'{API_PREFIX}/sync/history', GetSyncHistoryRequestExecutor(rpc_publisher)),
    ])
    aiohHttpServer.serve_forever()


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    main()

