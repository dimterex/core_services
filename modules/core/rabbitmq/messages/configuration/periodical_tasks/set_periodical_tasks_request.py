from modules.core.rabbitmq.messages.base_request import BaseMessage
from modules.core.rabbitmq.messages.configuration.periodical_task_model import PeriodicalTaskModel

SET_PERIODICAL_TASKS_REQUEST_MESSAGE_TYPE = 'set_periodical_tasks_request'
SET_PERIODICAL_TASKS_REQUEST_TASKS_PROPERTY = 'tasks'


class SetPeriodicalTasksRequest(BaseMessage):
    def __init__(self, tasks: list[PeriodicalTaskModel]):
        super().__init__(SET_PERIODICAL_TASKS_REQUEST_MESSAGE_TYPE)
        self.tasks = tasks

    def serialize(self):
        categories = []
        for category in self.tasks:
            categories.append(category.serialize())

        return self.to_json({
            SET_PERIODICAL_TASKS_REQUEST_TASKS_PROPERTY: categories,
        })

    @staticmethod
    def deserialize(payload):
        raw_tasks = payload[SET_PERIODICAL_TASKS_REQUEST_TASKS_PROPERTY]
        tasks: list[PeriodicalTaskModel] = []
        for task in raw_tasks:
            tasks.append(PeriodicalTaskModel.deserialize(task))

        return SetPeriodicalTasksRequest(tasks)
