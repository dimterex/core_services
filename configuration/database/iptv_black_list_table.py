from configuration.database.base_table import BaseTable
from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.configuration.iptv_black_list_item_model import IptvBlackListItemModel

ID_COLUMN_NAME = 'id'

IPTV_BLACK_LIST_TABLE_NAME = 'iptv_black_list'
IPTV_BLACK_LIST_VALUE_COLUMN_NAME = 'value'
IPTV_BLACK_LIST_TYPE_COLUMN_NAME = 'type'


class IptvBlackListTable(BaseTable):
    def __init__(self, logger: Logger_Service, path: str):
        super().__init__(IPTV_BLACK_LIST_TABLE_NAME, ID_COLUMN_NAME, logger, path)

    def get_initialize_table(self):
        return f'''CREATE TABLE IF NOT EXISTS {IPTV_BLACK_LIST_TABLE_NAME} (
                                {ID_COLUMN_NAME} INTEGER PRIMARY KEY AUTOINCREMENT,
                                {IPTV_BLACK_LIST_VALUE_COLUMN_NAME} TEXT NULL,
                                {IPTV_BLACK_LIST_TYPE_COLUMN_NAME} TEXT NULL);'''

    def get_black_list(self) -> list[IptvBlackListItemModel]:
        data = self.get_data()
        models = []
        for row in data:
            models.append(IptvBlackListItemModel(row[0], row[1], row[2]))
        return models

    def add_new_item(self):
        return self.insert({
            IPTV_BLACK_LIST_VALUE_COLUMN_NAME: str(),
        })
