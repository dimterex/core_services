import json

from modules.rabbitmq.messages.identificators import DISCORD_SEND_MESSAGE


class Send_Message:
    def __init__(self, promise_id, message):
        self.promise_id = promise_id
        self.message = message

    def to_json(self):
        dict_object = {
            'type': DISCORD_SEND_MESSAGE,
            'value': {
                'message': self.message,
                'promise_id': self.promise_id,
            }
        }
        return json.dumps(dict_object)

