import json

from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD, MESSAGE_TYPE

CREATE_SUBTASK_REQUEST_MESSAGE_TYPE = 'create_task_request'
CREATE_SUBTASK_REQUEST_NAME = 'name'
CREATE_SUBTASK_REQUEST_ROOT_ID = 'root_id'

class CreateSubTaskRequest:
    def __init__(self, task_name: str, parent_task_id: str):
        self.parent_task_id = parent_task_id
        self.task_name = task_name

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: CREATE_SUBTASK_REQUEST_MESSAGE_TYPE,
            MESSAGE_PAYLOAD: {
                CREATE_SUBTASK_REQUEST_NAME: self.task_name,
                CREATE_SUBTASK_REQUEST_ROOT_ID: self.parent_task_id,
            }
        }
        return json.dumps(dict_object)
