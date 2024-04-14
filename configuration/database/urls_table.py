from configuration.database.base_table import BaseTable
from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.configuration.url_model import UrlModel

ID_COLUMN_NAME = 'id'

URLS_TABLE_NAME = 'urls'
URLS_KEY_COLUMN_NAME = 'key'
URLS_VALUE_COLUMN_NAME = 'value'


class UrlsTable(BaseTable):
    def __init__(self, logger: Logger_Service, path: str):
        super().__init__(URLS_TABLE_NAME, ID_COLUMN_NAME, logger, path)

    def get_initialize_table(self):
        return f'''CREATE TABLE IF NOT EXISTS {URLS_TABLE_NAME} (
                                {ID_COLUMN_NAME} INTEGER PRIMARY KEY AUTOINCREMENT,
                                {URLS_KEY_COLUMN_NAME} TEXT NOT NULL,
                                {URLS_VALUE_COLUMN_NAME} TEXT NULL);'''

    def get_urls(self) -> list[UrlModel]:
        data = self.get_data()
        models = []
        for row in data:
            models.append(UrlModel(row[0], row[1], row[2]))
        return models

    def get_url(self, url_type: str):
        result = self.get_first({
            URLS_KEY_COLUMN_NAME: url_type
        })
        if result is None:
            raise Exception(f'Can not find url for {url_type}')

        return result[2]

    def set_urls(self, models: list[UrlModel]):
        params:  dict[int, dict] = {}

        for url in models:
            params[url.id] = {
                URLS_KEY_COLUMN_NAME: url.name,
                URLS_VALUE_COLUMN_NAME: url.key,
            }

        self.update(params)

    def add_new_url(self):
        return self.insert({
            URLS_KEY_COLUMN_NAME: str(),
            URLS_VALUE_COLUMN_NAME: str(),
        })
