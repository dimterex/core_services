import json

from modules.core.rabbitmq.messages.identificators import DISCORD_SEND_MESSAGE, MESSAGE_PAYLOAD, MESSAGE_TYPE


class Send_Message:
    def __init__(self, promise_id: str, message: str):
        self.promise_id = promise_id
        self.message = message

    def to_json(self):
        dict_object = {
            MESSAGE_TYPE: DISCORD_SEND_MESSAGE,
            MESSAGE_PAYLOAD: {
                'message': self.message,
                'promise_id': self.promise_id,
            }
        }
        return json.dumps(dict_object)

