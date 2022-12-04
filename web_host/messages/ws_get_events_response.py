import json

from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD, MESSAGE_TYPE

GET_EVENTS_RESPONSE_MESSAGE_TYPE = 'get_events_response'
GET_EVENTS_RESPONSE_EVENTS = 'events'


class Ws_Get_Events_Response():
    def __init__(self, worklogs: list[str]):
        self.worklogs = worklogs

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: GET_EVENTS_RESPONSE_MESSAGE_TYPE,
            MESSAGE_PAYLOAD: {
                GET_EVENTS_RESPONSE_EVENTS: self.worklogs,
            }
        }
        return json.dumps(dict_object)
