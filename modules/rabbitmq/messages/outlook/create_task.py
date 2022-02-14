import json

from modules.rabbitmq.messages.identificators import OUTLOOK_CREATE_TASK_MESSAGE


PROMISE_ID_PROPERTY = 'promise_id'
NAME_PROPERTY = 'name'
START_DATE_PROPERTY = 'start_date'
DURATION_PROPERTY = 'duration'
ISSUE_ID_PROPERTY = 'issue_id'


class Create_Task:
    def __init__(self, promise_id: str, name: str, start_date: str, duration: float, issue_id: str):
        self.issue_id = issue_id
        self.duration = duration
        self.start_date = start_date
        self.name = name
        self.promise_id = promise_id

    def to_json(self):
        dict_object = {
            'type': OUTLOOK_CREATE_TASK_MESSAGE,
            'value': {
                PROMISE_ID_PROPERTY: self.promise_id,
                NAME_PROPERTY: self.name,
                START_DATE_PROPERTY: self.start_date,
                DURATION_PROPERTY: self.duration,
                ISSUE_ID_PROPERTY: self.issue_id,
            }
        }
        return json.dumps(dict_object)

