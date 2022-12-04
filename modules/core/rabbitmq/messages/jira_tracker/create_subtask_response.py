import json

from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD, MESSAGE_TYPE

CREATE_SUBTASK_RESPONSE_MESSAGE_TYPE = 'create_task_response'
CREATE_SUBTASK_RESPONSE_TASK_ID_PROPERTY = 'id'

class CreateSubTaskResponse:
    def __init__(self, task_id: str):
        self.task_id = task_id

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: CREATE_SUBTASK_RESPONSE_MESSAGE_TYPE,
            MESSAGE_PAYLOAD: {
                CREATE_SUBTASK_RESPONSE_TASK_ID_PROPERTY: self.task_id,
            }
        }
        return json.dumps(dict_object)