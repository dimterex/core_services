
from modules.core.rabbitmq.messages.base_request import BaseMessage

CREATE_SUBTASK_REQUEST_MESSAGE_TYPE = 'create_task_request'
CREATE_SUBTASK_REQUEST_NAME = 'name'
CREATE_SUBTASK_REQUEST_ROOT_ID = 'root_id'


class CreateSubTaskRequest(BaseMessage):

    def __init__(self, task_name: str, parent_task_id: str):
        super().__init__(CREATE_SUBTASK_REQUEST_MESSAGE_TYPE)
        self.parent_task_id = parent_task_id
        self.task_name = task_name

    def serialize(self) -> dict:
        return self.to_json({
            CREATE_SUBTASK_REQUEST_NAME: self.task_name,
            CREATE_SUBTASK_REQUEST_ROOT_ID: self.parent_task_id,
        })
