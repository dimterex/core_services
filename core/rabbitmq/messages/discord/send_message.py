from core.rabbitmq.messages.base_request import BaseMessage

DISCORD_SEND_MESSAGE = 'send_message'


class Send_Message(BaseMessage):
    def __init__(self, promise_id: str, message: str):
        super().__init__(DISCORD_SEND_MESSAGE)
        self.promise_id = promise_id
        self.message = message

    def serialize(self) -> dict:
        return self.to_json({
            'message': self.message,
            'promise_id': self.promise_id,
        })
