import os
import time
import warnings

from configuration.database.configuration_storage import ConfigurationStorage
from configuration.handlers.credentials.get_credentials_request_handler import GetCredentialsRequestHandler
from configuration.handlers.iptv_black_list.add_black_list_item_request_handler import AddBlackListItemRequestHandler
from configuration.handlers.iptv_black_list.get_black_list_request_handler import GetBlackListRequestHandler
from configuration.handlers.iptv_black_list.remove_black_list_item__request_handler import \
    RemoveBlackListItemRequestHandler
from configuration.handlers.iptv_source.get_iptv_sources_request_handler import GetIptvSourcesRequestHandler
from configuration.handlers.meetings_caegories.add_new_meeting_category_request_handler import \
    AddNewMeetingCategoryRequestHandler
from configuration.handlers.meetings_caegories.remove_meeting_categories_request_handler import \
    RemoveMeetingCategoriesRequestHandler
from configuration.handlers.periodical_tasks.add_new_periodical_task_request_handler import \
    AddNewPeriodicalTaskRequestHandler
from configuration.handlers.periodical_tasks.get_periodical_tasks_request_handler import \
    GetPeriodicalTasksRequestHandler
from configuration.handlers.periodical_tasks.remove_periodical_tasks_request_handler import \
    RemovePeriodicalTasksRequestHandler
from configuration.handlers.periodical_tasks.set_periodical_tasks_request_handler import \
    SetPeriodicalTasksRequestHandler
from configuration.handlers.todoist_caegories.add_new_todoist_category_request_handler import \
    AddNewTodoistCategoryRequestHandler
from configuration.handlers.todoist_caegories.remove_todoist_categories_request_handler import \
    RemoveTodoistCategoriesRequestHandler
from configuration.handlers.tokens.add_new_token_request_handler import AddNewTokenRequestHandler
from configuration.handlers.tokens.get_token_request_handler import GetTokenRequestHandler
from configuration.handlers.tokens.get_tokens_request_handler import GetTokensRequestHandler
from configuration.handlers.tokens.remove_tokens_request_handler import RemoveTokensRequestHandler
from configuration.handlers.tokens.set_token_request_handler import SetTokenRequestHandler
from configuration.handlers.tokens.set_tokens_request_handler import SetTokensRequestHandler
from configuration.handlers.tracks.add_new_track_request_handler import AddNewTrackRequestHandler
from configuration.handlers.tracks.get_track_request_handler import GetTrackRequestHandler
from configuration.handlers.tracks.get_tracks_request_handler import GetTracksRequestHandler
from configuration.handlers.urls.add_new_url_request_handler import AddNewUrlRequestHandler
from configuration.handlers.urls.get_url_request_handler import GetUrlRequestHandler
from configuration.handlers.credentials.set_credentials_request_handler import SetCredentialsRequestHandler
from configuration.handlers.meetings_caegories.get_meeting_categories_request_handler import \
    GetMeetingCategoriesRequestHandler
from configuration.handlers.meetings_caegories.set_meeting_categories_request_handler import \
    SetMeetingCategoriesRequestHandler
from configuration.handlers.urls.get_urls_request_handler import GetUrlsRequestHandler
from configuration.handlers.urls.remove_url_request_handler import RemoveUrlsRequestHandler
from configuration.handlers.urls.set_url_request_handler import SetUrlRequestHandler
from configuration.handlers.todoist_caegories.get_todoits_categories_request_handler import \
    GetTodoistCategoriesRequestHandler
from configuration.handlers.todoist_caegories.set_todoist_categories_request_handler import \
    SetTodoitsCategoriesRequestHandler
from core.rabbitmq.messages.identificators import CONFIGURATION_QUEUE
from core.rabbitmq.rpc.rcp_api_controller import RpcApiController
from core.rabbitmq.rpc.rpc_consumer import RpcConsumer

from core.log_service.log_service import Logger_Service

RABBIT_CONNECTION_STRING = 'RABBIT_AMPQ_URL'
STORAGE_FOLDER_ENVIRON = 'STORAGE'


def main():
    ampq_url = os.environ[RABBIT_CONNECTION_STRING]
    storage_path = os.environ[STORAGE_FOLDER_ENVIRON]

    logger_service = Logger_Service()
    storage = ConfigurationStorage(storage_path, logger_service)

    api_controller = RpcApiController(logger_service)

    # credentials
    api_controller.subscribe(GetCredentialsRequestHandler(storage.credentials_table))
    api_controller.subscribe(SetCredentialsRequestHandler(storage.credentials_table))

    # urls
    api_controller.subscribe(GetUrlRequestHandler(storage.urls_table))
    api_controller.subscribe(GetUrlsRequestHandler(storage.urls_table))
    api_controller.subscribe(SetUrlRequestHandler(storage.urls_table))
    api_controller.subscribe(AddNewUrlRequestHandler(storage.urls_table))
    api_controller.subscribe(RemoveUrlsRequestHandler(storage.urls_table))

    # outlook
    api_controller.subscribe(GetMeetingCategoriesRequestHandler(storage.meeting_categories_table))
    api_controller.subscribe(SetMeetingCategoriesRequestHandler(storage.meeting_categories_table))
    api_controller.subscribe(AddNewMeetingCategoryRequestHandler(storage.meeting_categories_table))
    api_controller.subscribe(RemoveMeetingCategoriesRequestHandler(storage.meeting_categories_table))

    # todoist
    api_controller.subscribe(GetTodoistCategoriesRequestHandler(storage.todoist_categories_table))
    api_controller.subscribe(SetTodoitsCategoriesRequestHandler(storage.todoist_categories_table))
    api_controller.subscribe(AddNewTodoistCategoryRequestHandler(storage.todoist_categories_table))
    api_controller.subscribe(RemoveTodoistCategoriesRequestHandler(storage.todoist_categories_table))

    # tokens
    api_controller.subscribe(GetTokensRequestHandler(storage.tokens_table))
    api_controller.subscribe(GetTokenRequestHandler(storage.tokens_table))
    api_controller.subscribe(SetTokensRequestHandler(storage.tokens_table))
    api_controller.subscribe(SetTokenRequestHandler(storage.tokens_table))
    api_controller.subscribe(AddNewTokenRequestHandler(storage.tokens_table))
    api_controller.subscribe(RemoveTokensRequestHandler(storage.tokens_table))

    # periodical tasks
    api_controller.subscribe(GetPeriodicalTasksRequestHandler(storage.periodical_tasks_table))
    api_controller.subscribe(SetPeriodicalTasksRequestHandler(storage.periodical_tasks_table))
    api_controller.subscribe(AddNewPeriodicalTaskRequestHandler(storage.periodical_tasks_table))
    api_controller.subscribe(RemovePeriodicalTasksRequestHandler(storage.periodical_tasks_table))

    # tracks
    api_controller.subscribe(AddNewTrackRequestHandler(storage.tracks_table))
    api_controller.subscribe(GetTrackRequestHandler(storage.tracks_table))
    api_controller.subscribe(GetTracksRequestHandler(storage.tracks_table))

    # iptv
    api_controller.subscribe(AddBlackListItemRequestHandler(storage.iptv_black_list_table))
    api_controller.subscribe(GetBlackListRequestHandler(storage.iptv_black_list_table))
    api_controller.subscribe(RemoveBlackListItemRequestHandler(storage.iptv_black_list_table))
    api_controller.subscribe(GetIptvSourcesRequestHandler(storage.iptv_sources_table))

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
