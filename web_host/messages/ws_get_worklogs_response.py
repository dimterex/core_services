import json

from modules.core.rabbitmq.messages.identificators import PROMISE_ID_PROPERTY, MESSAGE_TYPE, MESSAGE_PAYLOAD

GET_WORKLOGS_RESPONSE_MESSAGE_TYPE = 'get_worklogs_response'
GET_WORKLOGS_RESPONSE_WORKLOGS = 'worklogs'


class WsGetWorklogsResponse:
    def __init__(self, events: list[str]):
        self.events = events

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: GET_WORKLOGS_RESPONSE_MESSAGE_TYPE,
            MESSAGE_PAYLOAD: {
                GET_WORKLOGS_RESPONSE_WORKLOGS: self.events,
            }
        }
        return json.dumps(dict_object)
