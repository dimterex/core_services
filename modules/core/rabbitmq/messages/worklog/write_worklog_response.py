import datetime
import json

from modules.core.rabbitmq.messages.identificators import MESSAGE_TYPE, MESSAGE_PAYLOAD

WORKLOG_WRITE_MESSAGE_RESPONSE_TYPE = 'write_worklog_response'
WORKLOG_WRITE_MESSAGE_RESPONSE_RESULT_PROPERTY = 'result'

class Write_Worklog_Response:
    def __init__(self, result: str):
        self.result = result

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: WORKLOG_WRITE_MESSAGE_RESPONSE_TYPE,
            MESSAGE_PAYLOAD: {
                WORKLOG_WRITE_MESSAGE_RESPONSE_RESULT_PROPERTY: str(self.result),
            }
        }
        return json.dumps(dict_object)

