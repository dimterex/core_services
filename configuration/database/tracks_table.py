from configuration.database.base_table import BaseTable
from modules.core.log_service.log_service import Logger_Service

ID_COLUMN_NAME = 'id'

TABLE_NAME = 'yandex_music_downloaded'
TRACK_ID_COLUMN_NAME = 'track_id'
TRACK_NAME_COLUMN_NAME = 'name'


class YandexMusicTable(BaseTable):
    def __init__(self, logger: Logger_Service, path: str):
        super().__init__(TABLE_NAME, ID_COLUMN_NAME, logger, path)

    def get_initialize_table(self):
        return f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                                {ID_COLUMN_NAME} INTEGER PRIMARY KEY AUTOINCREMENT,
                                {TRACK_ID_COLUMN_NAME} TEXT NOT NULL,
                                {TRACK_NAME_COLUMN_NAME} TEXT NULL);'''

    def get_urls(self) -> list[UrlModel]:
        data = self.get_data()
        models = []
        for row in data:
            models.append(UrlModel(row[0], row[1], row[1]))
        return models

    def get_url(self, url_type: str):
        result = self.get_first({
            KEY_COLUMN_NAME: url_type
        })
        if result is None:
            raise Exception(f'Can not find url for {url_type}')

        return result[2]

    def set_urls(self, models: list[UrlModel]):
        params:  dict[int, dict] = {}

        for url in models:
            params[url.id] = {
                KEY_COLUMN_NAME: url.name,
                VALUE_COLUMN_NAME: url.key,
            }

        self.update(params)

    def add_new_url(self):
        return self.insert({
            KEY_COLUMN_NAME: str(),
            VALUE_COLUMN_NAME: str(),
        })
