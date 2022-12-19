from modules.core.rabbitmq.messages.base_request import BaseMessage

GET_CREDENTIALS_REQUEST_MESSAGE_TYPE = 'get_credentials_request'


class GetCredentialsRequest(BaseMessage):

    def __init__(self):
        super().__init__(GET_CREDENTIALS_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
