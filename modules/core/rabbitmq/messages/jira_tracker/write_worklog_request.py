import json

from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD, MESSAGE_TYPE

WRITE_WORKLOG_REQUEST_MESSAGE_TYPE = 'write_worklog_request'
WRITE_WORKLOG_REQUEST_WORKLOGS = 'worklogs'


class WriteWorklogsRequest:
    def __init__(self, worklogs: []):
        self.worklogs = worklogs

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: WRITE_WORKLOG_REQUEST_MESSAGE_TYPE,
            MESSAGE_PAYLOAD: {
                WRITE_WORKLOG_REQUEST_WORKLOGS: self.worklogs,
            }
        }
        return json.dumps(dict_object)
