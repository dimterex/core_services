import json

from modules.core.rabbitmq.messages.identificators import PROMISE_ID_PROPERTY, MESSAGE_TYPE, MESSAGE_PAYLOAD
from todoist.models.task_entry import Task_Entry


GET_COMPLETED_TASK_RESPONSE_MESSAGE_TYPE = 'get_completed_tasks_response'
GET_COMPLETED_TASK_RESPONSE_ISSUES_PROPERTY = 'issues'


class GetCompletedTasksResponse:
    def __init__(self, issues: list[Task_Entry]):
        self.issues = issues

    def to_json(self):
        dict_object = {
            GET_COMPLETED_TASK_RESPONSE_ISSUES_PROPERTY: self.issues
        }
        return json.dumps(dict_object)
