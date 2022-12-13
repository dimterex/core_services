import json
from datetime import datetime

from modules.core.rabbitmq.messages.identificators import MESSAGE_TYPE, MESSAGE_PAYLOAD

GET_HISTORY_BY_DATE_REQUEST_TYPE = 'get_history_request'
GET_HISTORY_BY_DATE_REQUEST_DAY_PROPERTY = 'day'


class GetHistoryByDateRequest:
    def __init__(self, start_day: datetime):
        self.start_day = start_day

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: GET_HISTORY_BY_DATE_REQUEST_TYPE,
            MESSAGE_PAYLOAD: {
                GET_HISTORY_BY_DATE_REQUEST_DAY_PROPERTY: str(self.start_day),
            }
        }
        return json.dumps(dict_object)

