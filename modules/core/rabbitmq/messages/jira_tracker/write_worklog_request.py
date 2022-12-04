import json

from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD, MESSAGE_TYPE
from modules.models.worklog import Worklog

WRITE_WORKLOG_REQUEST_MESSAGE_TYPE = 'write_worklog_request'
WRITE_WORKLOG_REQUEST_WORKLOGS = 'worklogs'


class WriteWorklogsRequest:
    def __init__(self, worklogs: list[Worklog]):
        self.worklogs = worklogs

    def to_json(self):
        worklogs = []
        for worklog in self.worklogs:
            rawIssue = []
            rawIssue.append('{')
            rawIssue.append(f'"name": "{worklog.name}",')
            rawIssue.append(f'"date": "{worklog.date}",')
            rawIssue.append(f'"tracker_id": "{worklog.issue_id}",')
            rawIssue.append(f'"duration": "{worklog.duration}"')
            rawIssue.append('}')
            worklogs.append(''.join(rawIssue))

        rawWorklogs = ','.join(worklogs)
        rawWorklogs = f'[{rawWorklogs}]'

        dict_object = {
            MESSAGE_TYPE: WRITE_WORKLOG_REQUEST_MESSAGE_TYPE,
            MESSAGE_PAYLOAD: {
                WRITE_WORKLOG_REQUEST_WORKLOGS: rawWorklogs,
            }
        }
        return json.dumps(dict_object)
