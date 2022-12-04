import datetime
import json

from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD, MESSAGE_TYPE

WORKLOG_WRITE_MESSAGE_REQUEST_TYPE = 'write_worklog_request'
WORKLOG_WRITE_MESSAGE_REQUEST_DAY_PROPERTY = 'start_day'

class Write_Worklog_Request:
    def __init__(self, start_day: datetime.datetime):
        self.start_day = start_day

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: WORKLOG_WRITE_MESSAGE_REQUEST_TYPE,
            MESSAGE_PAYLOAD: {
                WORKLOG_WRITE_MESSAGE_REQUEST_DAY_PROPERTY: str(self.start_day),
            }
        }
        return json.dumps(dict_object)

