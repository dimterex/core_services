from modules.core.rabbitmq.messages.base_request import BaseMessage

GET_TOKEN_REQUEST_MESSAGE_TYPE = 'get_token_request'
GET_TOKEN_REQUEST_KEY_PROPERTY = 'key'


class GetTokenRequest(BaseMessage):
    def __init__(self, key: str):
        super().__init__(GET_TOKEN_REQUEST_MESSAGE_TYPE)
        self.key = key

    def serialize(self):
        return self.to_json({
            GET_TOKEN_REQUEST_KEY_PROPERTY: self.key,
        })

    @staticmethod
    def deserialize(payload):
        token = payload[GET_TOKEN_REQUEST_KEY_PROPERTY]
        return GetTokenRequest(token)
