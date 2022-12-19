from modules.core.rabbitmq.messages.identificators import MESSAGE_PAYLOAD, MESSAGE_TYPE


class BaseMessage:
    def __init__(self, message_type: str):
        self.message_type = message_type

    def serialize(self) -> dict:
        raise Exception('Not implemented')

    def to_json(self, payload: dict) -> dict:
        return {
            MESSAGE_TYPE: self.message_type,
            MESSAGE_PAYLOAD: payload
        }
