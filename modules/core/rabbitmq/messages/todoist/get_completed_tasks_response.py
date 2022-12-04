import json

from modules.core.rabbitmq.messages.identificators import PROMISE_ID_PROPERTY, MESSAGE_TYPE, MESSAGE_PAYLOAD
from todoist.models.task_entry import Task_Entry


GET_COMPLETED_TASK_RESPONSE_MESSAGE_TYPE = 'get_completed_tasks_response'
GET_COMPLETED_TASK_RESPONSE_ISSUES_PROPERTY = 'issues'


class GetCompletedTasksResponse:
    def __init__(self, issues: list[Task_Entry]):
        self.issues = issues

    def to_json(self):
        issues = []
        for issue in self.issues:
            rawIssue = []
            rawIssue.append('{')
            rawIssue.append(f'"name": "{issue.name}",')
            rawIssue.append(f'"category": "{issue.category}",')
            rawIssue.append(f'"tracker_id": "{issue.jira_issue}",')
            rawIssue.append(f'"id": "{issue.id}"')
            rawIssue.append('}')
            issues.append(''.join(rawIssue))

        rawIssues = ','.join(issues)
        rawIssues = f'[{rawIssues}]'

        dict_object = {
            MESSAGE_TYPE: GET_COMPLETED_TASK_RESPONSE_MESSAGE_TYPE,
            MESSAGE_PAYLOAD: {
                GET_COMPLETED_TASK_RESPONSE_ISSUES_PROPERTY: rawIssues
            }
        }
        return json.dumps(dict_object)
