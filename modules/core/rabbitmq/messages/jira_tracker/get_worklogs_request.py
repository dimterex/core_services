import json

from modules.core.rabbitmq.messages.identificators import PROMISE_ID_PROPERTY, QUEUE_RESPOND, MESSAGE_PAYLOAD, \
    MESSAGE_TYPE

GET_WORKLOGS_REQUEST_MESSAGE_TYPE = 'get_worklogs_request'
GET_WORKLOGS_REQUEST_YEAR = 'year'
GET_WORKLOGS_REQUEST_MONTH = 'month'


class GetWorklogsRequest:
    def __init__(self, year: int, month: int):
        self.year = year
        self.month = month

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: GET_WORKLOGS_REQUEST_MESSAGE_TYPE,
            MESSAGE_PAYLOAD: {
                GET_WORKLOGS_REQUEST_YEAR: self.year,
                GET_WORKLOGS_REQUEST_MONTH: self.month,
            }
        }
        return json.dumps(dict_object)
