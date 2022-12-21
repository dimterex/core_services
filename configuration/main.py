import os
import time
import warnings

from configuration.database.configuration_storage import ConfigurationStorage
from configuration.handlers.credentials.get_credentials_request_handler import GetCredentialsRequestHandler
from configuration.handlers.periodical_tasks.get_periodical_tasks_request_handler import \
    GetPeriodicalTasksRequestHandler
from configuration.handlers.periodical_tasks.set_periodical_tasks_request_handler import \
    SetPeriodicalTasksRequestHandler
from configuration.handlers.tokens.get_token_request_handler import GetTokenRequestHandler
from configuration.handlers.tokens.get_tokens_request_handler import GetTokensRequestHandler
from configuration.handlers.tokens.set_token_request_handler import SetTokenRequestHandler
from configuration.handlers.tokens.set_tokens_request_handler import SetTokensRequestHandler
from configuration.handlers.urls.get_url_request_handler import GetUrlRequestHandler
from configuration.handlers.credentials.set_credentials_request_handler import SetCredentialsRequestHandler
from configuration.handlers.meetings_caegories.get_meeting_categories_request_handler import \
    GetMeetingCategoriesRequestHandler
from configuration.handlers.meetings_caegories.set_meeting_categories_request_handler import \
    SetMeetingCategoriesRequestHandler
from configuration.handlers.urls.get_urls_request_handler import GetUrlsRequestHandler
from configuration.handlers.urls.set_url_request_handler import SetUrlRequestHandler
from configuration.handlers.todoist_caegories.get_todoits_categories_request_handler import \
    GetTodoistCategoriesRequestHandler
from configuration.handlers.todoist_caegories.set_todoist_categories_request_handler import \
    SetTodoitsCategoriesRequestHandler
from modules.core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from modules.core.rabbitmq.rpc.rpc_consumer import RpcConsumer

from modules.core.log_service.log_service import Logger_Service

RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'
STORAGE_FOLDER_ENVIRON = 'STORAGE'


def main():
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    storage_path = os.environ[STORAGE_FOLDER_ENVIRON]

    logger_service = Logger_Service()
    storage = ConfigurationStorage(storage_path, logger_service)

    api_controller = RpcApiController(logger_service)

    api_controller.subscribe(GetCredentialsRequestHandler(storage))
    api_controller.subscribe(SetCredentialsRequestHandler(storage))

    api_controller.subscribe(GetUrlRequestHandler(storage))
    api_controller.subscribe(GetUrlsRequestHandler(storage))
    api_controller.subscribe(SetUrlRequestHandler(storage))

    api_controller.subscribe(GetMeetingCategoriesRequestHandler(storage))
    api_controller.subscribe(SetMeetingCategoriesRequestHandler(storage))

    api_controller.subscribe(GetTodoistCategoriesRequestHandler(storage))
    api_controller.subscribe(SetTodoitsCategoriesRequestHandler(storage))

    api_controller.subscribe(GetTokensRequestHandler(storage))
    api_controller.subscribe(GetTokenRequestHandler(storage))
    api_controller.subscribe(SetTokensRequestHandler(storage))
    api_controller.subscribe(SetTokenRequestHandler(storage))

    api_controller.subscribe(GetPeriodicalTasksRequestHandler(storage))
    api_controller.subscribe(SetPeriodicalTasksRequestHandler(storage))

    rcp = RpcConsumer(ampq_url, CONFIGURATION_QUEUE, api_controller)
    rcp.start()


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
