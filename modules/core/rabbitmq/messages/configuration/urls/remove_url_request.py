from modules.core.rabbitmq.messages.base_request import BaseMessage

REMOVE_URLS_REQUEST_MESSAGE_TYPE = 'remove_urls_request'
REMOVE_URLS_REQUEST_IDS = 'ids'


class RemoveUrlsRequest(BaseMessage):

    def __init__(self, ids: list[int]):
        super().__init__(REMOVE_URLS_REQUEST_MESSAGE_TYPE)
        self.ids = ids

    def serialize(self):
        return self.to_json({
            REMOVE_URLS_REQUEST_IDS: self.ids
        })

    @staticmethod
    def deserialize(payload):
        ids = payload[REMOVE_URLS_REQUEST_IDS]
        return RemoveUrlsRequest(ids)
