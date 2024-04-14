import datetime

from core.rabbitmq.messages.base_request import BaseMessage

COMPLETED_TASKS_REQUEST_MESSAGE_TYPE = 'get_completed_tasks_request'
COMPLETED_TASKS_REQUEST_DATE_PROPERTY = 'date'


class GetCompletedTasksRequest(BaseMessage):

    def __init__(self, date: datetime.datetime):
        super().__init__(COMPLETED_TASKS_REQUEST_MESSAGE_TYPE)
        self.date: str = f'{date.year}/{date.month}/{date.day}'

    def serialize(self) -> dict:
        return self.to_json({
            COMPLETED_TASKS_REQUEST_DATE_PROPERTY: self.date,
        })
