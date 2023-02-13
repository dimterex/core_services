from configuration.database.base_table import BaseTable
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.configuration.category_model import CategoryModel

ID_COLUMN_NAME = "id"
MEETING_CATEGORIES_TABLE_NAME = 'meeting_categories'
MEETING_CATEGORIES_NAME_COLUMN_NAME = 'name'
MEETING_CATEGORIES_TRACKER_ID_COLUMN_NAME = 'tracker_id'
MEETING_CATEGORIES_LINK_COLUMN_NAME = 'link'


class MeetingCategoriesTable(BaseTable):
    def __init__(self, logger: Logger_Service, path: str):
        super().__init__(MEETING_CATEGORIES_TABLE_NAME, ID_COLUMN_NAME, logger, path)

    def get_initialize_table(self):
        return f'''CREATE TABLE IF NOT EXISTS {MEETING_CATEGORIES_TABLE_NAME} (
                                {ID_COLUMN_NAME} INTEGER PRIMARY KEY AUTOINCREMENT,
                                {MEETING_CATEGORIES_NAME_COLUMN_NAME} TEXT NOT NULL,
                                {MEETING_CATEGORIES_TRACKER_ID_COLUMN_NAME} TEXT NULL,
                                {MEETING_CATEGORIES_LINK_COLUMN_NAME} TEXT NULL);'''

    def get_meeting_categories(self) -> list[CategoryModel]:

        data = self.get_data()
        models = []
        for row in data:
            models.append(CategoryModel(row[0], row[1], row[2], row[3]))
        return models

    def add_new_meeting_category(self) -> int:
        params = {
            MEETING_CATEGORIES_NAME_COLUMN_NAME: str(),
            MEETING_CATEGORIES_TRACKER_ID_COLUMN_NAME: str(),
            MEETING_CATEGORIES_LINK_COLUMN_NAME: str(),
        }

        return self.insert(params)

    def remove_meeting_categories(self, ids: list[int]):
        self.remove(ids)

    def set_meeting_categories(self, categories: list[CategoryModel]):
        params:  dict[int, dict] = {}

        for category in categories:
            params[category.id] = {
                MEETING_CATEGORIES_NAME_COLUMN_NAME: category.name,
                MEETING_CATEGORIES_TRACKER_ID_COLUMN_NAME: category.tracker_id,
                MEETING_CATEGORIES_LINK_COLUMN_NAME: category.link,
            }

        self.update(params)
