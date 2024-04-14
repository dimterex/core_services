from core.rabbitmq.messages.base_request import BaseMessage
from core.rabbitmq.messages.configuration.url_model import UrlModel

SET_URL_REQUEST_MESSAGE_TYPE = 'set_urls_request'
SET_URL_REQUEST_MODELS_MESSAGE_PROPERTY = 'models'


class SetUrlsRequest(BaseMessage):
    def __init__(self, models: list[UrlModel]):
        super().__init__(SET_URL_REQUEST_MESSAGE_TYPE)
        self.models = models

    def serialize(self):
        return self.to_json({
            SET_URL_REQUEST_MODELS_MESSAGE_PROPERTY: self.models,
        })

    @staticmethod
    def deserialize(payload):
        urls = payload[SET_URL_REQUEST_MODELS_MESSAGE_PROPERTY]
        return SetUrlsRequest(urls)
