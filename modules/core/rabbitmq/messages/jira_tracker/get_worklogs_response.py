import json

from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD, MESSAGE_TYPE

GET_WORKLOGS_RESPONSE_MESSAGE_TYPE = 'get_worklogs_response'
GET_WORKLOGS_RESPONSE_WORKLOGS = 'worklogs'


class GetWorklogsResponse:
    def __init__(self, worklogs: list):
        self.worklogs = worklogs

    def to_json(self):
        worklogs = []
        for worklog in self.worklogs:
            worklogs.append(worklog.to_json())

        rawWorklogs = ','.join(worklogs)
        rawWorklogs = f'[{rawWorklogs}]'

        dict_object = {
            MESSAGE_TYPE: GET_WORKLOGS_RESPONSE_MESSAGE_TYPE,
            MESSAGE_PAYLOAD: {
                GET_WORKLOGS_RESPONSE_WORKLOGS: rawWorklogs,
            }
        }
        return json.dumps(dict_object)
