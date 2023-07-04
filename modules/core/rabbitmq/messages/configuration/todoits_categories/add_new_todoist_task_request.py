from modules.core.rabbitmq.messages.base_request import BaseMessage

ADD_NEW_TODOIST_TASK_REQUEST_MESSAGE_TYPE = 'add_new_todoist_task_request'
ADD_NEW_TODOIST_TASK_REQUEST_NAME = 'name'
ADD_NEW_TODOIST_TASK_REQUEST_ISSUE_ID = 'issue_id'


class AddNewTodoistTaskRequest(BaseMessage):

    def __init__(self, name: str, issue_id: str):
        super().__init__(ADD_NEW_TODOIST_TASK_REQUEST_MESSAGE_TYPE)
        self.name = name
        self.issue_id = issue_id

    def serialize(self):
        return self.to_json({
            ADD_NEW_TODOIST_TASK_REQUEST_NAME: self.name,
            ADD_NEW_TODOIST_TASK_REQUEST_ISSUE_ID: self.issue_id,
        })

    @staticmethod
    def deserialize(payload):
        name = payload[ADD_NEW_TODOIST_TASK_REQUEST_NAME]
        issue_id = payload[ADD_NEW_TODOIST_TASK_REQUEST_ISSUE_ID]
        return AddNewTodoistTaskRequest(name, issue_id)
