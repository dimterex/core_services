from configuration.database.base_table import BaseTable
from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.configuration.iptv_source_model import IptvSourceModel

ID_COLUMN_NAME = 'id'

IPTV_SOURCES_TABLE_NAME = 'iptv_sources'
IPTV_SOURCES_VALUE_COLUMN_NAME = 'value'


class IptvSourcesTable(BaseTable):
    def __init__(self, logger: Logger_Service, path: str):
        super().__init__(IPTV_SOURCES_TABLE_NAME, ID_COLUMN_NAME, logger, path)

    def get_initialize_table(self):
        return f'''CREATE TABLE IF NOT EXISTS {IPTV_SOURCES_TABLE_NAME} (
                                {ID_COLUMN_NAME} INTEGER PRIMARY KEY AUTOINCREMENT,
                                {IPTV_SOURCES_VALUE_COLUMN_NAME} TEXT NULL);'''

    def get_sources(self) -> list[IptvSourceModel]:
        data = self.get_data()
        models = []
        for row in data:
            models.append(IptvSourceModel(row[0], row[1]))
        return models

    def add_new_item(self):
        return self.insert({
            IPTV_SOURCES_VALUE_COLUMN_NAME: str(),
        })
