from core.rabbitmq.messages.base_request import BaseMessage
from core.rabbitmq.messages.configuration.token_model import TokenModel

SET_TOKEN_REQUEST_MESSAGE_TYPE = 'set_token_request'
SET_TOKEN_REQUEST_TOKEN_PROPERTY = 'token'


class SetTokenRequest(BaseMessage):
    def __init__(self, token: TokenModel):
        super().__init__(SET_TOKEN_REQUEST_MESSAGE_TYPE)
        self.token = token

    def serialize(self):
        return self.to_json(self.token.serialize())

    @staticmethod
    def deserialize(payload):
        raw_token = payload[SET_TOKEN_REQUEST_TOKEN_PROPERTY]
        return SetTokenRequest(TokenModel.deserialize(raw_token))
