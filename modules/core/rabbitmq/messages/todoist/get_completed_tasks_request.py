import datetime
import json

from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD, MESSAGE_TYPE

COMPLETED_TASKS_REQUEST_MESSAGE_TYPE = 'get_completed_tasks_request'
COMPLETED_TASKS_REQUEST_DATE_PROPERTY = 'date'


class GetCompletedTasksRequest:
    def __init__(self, date: datetime.datetime):
        self.date: str = f'{date.year}/{date.month}/{date.day}'

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: COMPLETED_TASKS_REQUEST_MESSAGE_TYPE,
            MESSAGE_PAYLOAD: {
                COMPLETED_TASKS_REQUEST_DATE_PROPERTY: self.date,
            }
        }
        return json.dumps(dict_object)
