from core.rabbitmq.messages.base_request import BaseMessage
from core.rabbitmq.messages.configuration.token_model import TokenModel

SET_TOKENS_REQUEST_MESSAGE_TYPE = 'set_tokens_request'
SET_TOKENS_REQUEST_CATEGORIES_PROPERTY = 'tokens'


class SetTokensRequest(BaseMessage):
    def __init__(self, tokens: list[TokenModel]):
        super().__init__(SET_TOKENS_REQUEST_MESSAGE_TYPE)
        self.tokens = tokens

    def serialize(self):
        tokens = []
        for category in self.tokens:
            tokens.append(category.serialize())

        return self.to_json({
            SET_TOKENS_REQUEST_CATEGORIES_PROPERTY: tokens,
        })

    @staticmethod
    def deserialize(payload):
        raw_tokens = payload[SET_TOKENS_REQUEST_CATEGORIES_PROPERTY]
        tokens: list[TokenModel] = []
        for category in raw_tokens:
            tokens.append(TokenModel.deserialize(category))

        return SetTokensRequest(tokens)
