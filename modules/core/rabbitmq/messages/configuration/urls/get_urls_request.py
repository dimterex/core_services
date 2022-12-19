from modules.core.rabbitmq.messages.base_request import BaseMessage

GET_URL_REQUEST_MESSAGE_TYPE = 'get_url_request'
GET_URL_REQUEST_URL_TYPE = 'type'


class GetUrlRequest(BaseMessage):
    def __init__(self, url_type: str):
        super().__init__(GET_URL_REQUEST_MESSAGE_TYPE)
        self.url_type = url_type

    def serialize(self):
        return self.to_json({
            GET_URL_REQUEST_URL_TYPE: self.url_type,
        })

    @staticmethod
    def deserialize(payload):
        url_type = payload[GET_URL_REQUEST_URL_TYPE]
        return GetUrlRequest(url_type)
