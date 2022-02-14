import json

from modules.rabbitmq.messages.identificators import GET_NEXT_MEETING_MESSAGE

PROMISE_ID_PROPERTY = 'promise_id'


class Get_Next_Meeting:
    def __init__(self, promise_id: str):
        self.promise_id = promise_id

    def to_json(self):
        dict_object = {
            'type': GET_NEXT_MEETING_MESSAGE,
            'value': {
                PROMISE_ID_PROPERTY: self.promise_id,
            }
        }
        return json.dumps(dict_object)

