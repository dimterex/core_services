from core.rabbitmq.messages.base_request import BaseMessage

ADD_NEW_TOKEN_REQUEST_MESSAGE_TYPE = 'add_new_token_request'


class AddNewTokenRequest(BaseMessage):

    def __init__(self):
        super().__init__(ADD_NEW_TOKEN_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
