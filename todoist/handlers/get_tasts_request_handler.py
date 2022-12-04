from todoist_api_python.api import TodoistAPI

from modules.core.rabbitmq.publisher import Publisher


class GetTasksRequestHandler:
    def __init__(self, todoist: TodoistAPI, publisher: Publisher):
        self.publisher = publisher
        self.todoist = todoist

    def execute(self, promise_id: int, date: str):
        pass
