import os

from configuration.database.credentials_table import CredentialsTable
from configuration.database.iptv_black_list_table import IptvBlackListTable
from configuration.database.iptv_sources_table import IptvSourcesTable
from configuration.database.meeting_categories_table import MeetingCategoriesTable
from configuration.database.periodical_tasks_table import PeriodicalTasksTable
from configuration.database.todoist_categories_table import TodoistCategoriesTable
from configuration.database.tokens_table import TokensTable
from configuration.database.tracks_table import TracksTable
from configuration.database.urls_table import UrlsTable
from core.log_service.log_service import Logger_Service

from core.sqlite.base_storage import BaseStorage

DATABASE_NAME = 'configuration_storage.db'


class ConfigurationStorage(BaseStorage):
    def __init__(self, path: str, logger: Logger_Service):
        path = os.path.join(path, DATABASE_NAME)
        self.meeting_categories_table = MeetingCategoriesTable(logger, path)
        self.credentials_table = CredentialsTable(logger, path)
        self.urls_table = UrlsTable(logger, path)
        self.todoist_categories_table = TodoistCategoriesTable(logger, path)
        self.tokens_table = TokensTable(logger, path)
        self.periodical_tasks_table = PeriodicalTasksTable(logger, path)
        self.tracks_table = TracksTable(logger, path)
        self.iptv_black_list_table = IptvBlackListTable(logger, path)
        self.iptv_sources_table = IptvSourcesTable(logger, path)
        super().__init__(logger, path)

    def get_create_table_request(self) -> list[str]:
        return [
            self.credentials_table.get_initialize_table(),
            self.urls_table.get_initialize_table(),
            self.meeting_categories_table.get_initialize_table(),
            self.todoist_categories_table.get_initialize_table(),
            self.tokens_table.get_initialize_table(),
            self.periodical_tasks_table.get_initialize_table(),
            self.tracks_table.get_initialize_table(),
            self.iptv_black_list_table.get_initialize_table(),
            self.iptv_sources_table.get_initialize_table(),
        ]
