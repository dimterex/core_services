from configuration.database.base_table import BaseTable
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.configuration.periodical_task_model import PeriodicalTaskModel

ID_COLUMN_NAME = 'id'

PERIODICAL_TASKS_TABLE_NAME = 'periodical_task'
PERIODICAL_TASKS_NAME_COLUMN_NAME = 'name'
PERIODICAL_TASKS_TRACKER_ID_COLUMN_NAME = 'tracker_id'
PERIODICAL_TASKS_DURATION_COLUMN_NAME = 'duration'


class PeriodicalTasksTable(BaseTable):
    def __init__(self, logger: Logger_Service, path: str):
        super().__init__(PERIODICAL_TASKS_TABLE_NAME, ID_COLUMN_NAME, logger, path)

    def get_initialize_table(self):
        return f'''CREATE TABLE IF NOT EXISTS {PERIODICAL_TASKS_TABLE_NAME} (
                                {ID_COLUMN_NAME} INTEGER PRIMARY KEY AUTOINCREMENT,
                                {PERIODICAL_TASKS_NAME_COLUMN_NAME} TEXT NOT NULL,
                                {PERIODICAL_TASKS_TRACKER_ID_COLUMN_NAME} TEXT NOT NULL,
                                {PERIODICAL_TASKS_DURATION_COLUMN_NAME} NUMERIC NOT NULL);'''

    def get_periodical_tasks(self) -> list[PeriodicalTaskModel]:
        data = self.get_data()
        models = []
        for row in data:
            models.append(PeriodicalTaskModel(row[0], row[1], row[2], row[3]))
        return models

    def set_periodical_tasks(self, tasks: list[PeriodicalTaskModel]):
        params:  dict[int, dict] = {}

        for task in tasks:
            params[task.id] = {
                PERIODICAL_TASKS_NAME_COLUMN_NAME: task.name,
                PERIODICAL_TASKS_TRACKER_ID_COLUMN_NAME: task.tracker_id,
                PERIODICAL_TASKS_DURATION_COLUMN_NAME: task.duration,
            }

        self.update(params)

    def add_new_task(self):
        return self.insert({
            PERIODICAL_TASKS_NAME_COLUMN_NAME: str(),
            PERIODICAL_TASKS_TRACKER_ID_COLUMN_NAME: str(),
            PERIODICAL_TASKS_DURATION_COLUMN_NAME: str(),
        })
