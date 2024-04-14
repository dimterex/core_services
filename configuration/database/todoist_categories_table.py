from configuration.database.base_table import BaseTable
from core.log_service.log_service import Logger_Service
from core.rabbitmq.messages.configuration.category_model import CategoryModel

ID_COLUMN_NAME = 'id'

TODOIST_LABELS_TABLE_NAME = 'todoist_labels'
TODOIST_CATEGORIES_NAME_COLUMN_NAME = 'name'
TODOIST_CATEGORIES_TRACKER_ID_COLUMN_NAME = 'tracker_id'
TODOIST_CATEGORIES_LINK_COLUMN_NAME = 'link'


class TodoistCategoriesTable(BaseTable):
    def __init__(self, logger: Logger_Service, path: str):
        super().__init__(TODOIST_LABELS_TABLE_NAME, ID_COLUMN_NAME, logger, path)

    def get_initialize_table(self):
        return f'''CREATE TABLE IF NOT EXISTS {TODOIST_LABELS_TABLE_NAME} (
                                {ID_COLUMN_NAME} INTEGER PRIMARY KEY AUTOINCREMENT,
                                {TODOIST_CATEGORIES_NAME_COLUMN_NAME} TEXT NOT NULL,
                                {TODOIST_CATEGORIES_TRACKER_ID_COLUMN_NAME} TEXT NOT NULL,
                                {TODOIST_CATEGORIES_LINK_COLUMN_NAME} TEXT NULL);'''

    def get_task_categories(self) -> list[CategoryModel]:
        data = self.get_data()
        models = []
        for row in data:

            models.append(CategoryModel(row[0], row[1], row[2], row[3]))
        return models

    def add_new_category(self) -> int:
        params = {
            TODOIST_CATEGORIES_NAME_COLUMN_NAME: str(),
            TODOIST_CATEGORIES_TRACKER_ID_COLUMN_NAME: str(),
            TODOIST_CATEGORIES_LINK_COLUMN_NAME: str(),
        }

        return self.insert(params)

    def remove_todoist_categories(self, ids: list[int]):
        self.remove(ids)

    def set_todoist_categories(self, categories: list[CategoryModel]):
        params:  dict[int, dict] = {}

        for category in categories:
            params[category.id] = {
                TODOIST_CATEGORIES_NAME_COLUMN_NAME: category.name,
                TODOIST_CATEGORIES_TRACKER_ID_COLUMN_NAME: category.tracker_id,
                TODOIST_CATEGORIES_LINK_COLUMN_NAME: category.link,
            }

        self.update(params)
