import json
from datetime import datetime

from modules.core.rabbitmq.messages.identificators import MESSAGE_TYPE, MESSAGE_PAYLOAD

GET_CALENDAR_BY_DATE_REQUEST = 'get_calendar_by_date_request'
GET_CALENDAR_DATE_PROPERTY = 'date'


class GetEventsByDateRequest:
    def __init__(self, date: datetime):
        self.date = str(date)

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: GET_CALENDAR_BY_DATE_REQUEST,
            MESSAGE_PAYLOAD: {
                GET_CALENDAR_DATE_PROPERTY: self.date,
            }
        }
        return json.dumps(dict_object)

