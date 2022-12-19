from modules.core.rabbitmq.messages.base_request import BaseMessage

GET_TOKENS_REQUEST_MESSAGE_TYPE = 'get_tokens_request'


class GetTokensRequest(BaseMessage):

    def __init__(self):
        super().__init__(GET_TOKENS_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
