from core.rabbitmq.messages.base_request import BaseMessage

GET_URLS_REQUEST_MESSAGE_TYPE = 'get_urls_request'


class GetUrlsRequest(BaseMessage):
    def __init__(self):
        super().__init__(GET_URLS_REQUEST_MESSAGE_TYPE)

    def serialize(self):
        return self.to_json(None)
