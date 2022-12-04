import json

from modules.core.rabbitmq.messages.identificators import PROMISE_ID_PROPERTY, MESSAGE_PAYLOAD, MESSAGE_TYPE

GetTasksRequest_MESSAGE_TYPE = 'get_tasks_request'


class GetTasksRequest:
    def __init__(self, promise_id: int, date: str):
        self.promise_id = promise_id
        self.date = date

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: GetTasksRequest_MESSAGE_TYPE,
            MESSAGE_PAYLOAD: {
                PROMISE_ID_PROPERTY: self.promise_id,
            }
        }
        return json.dumps(dict_object)
