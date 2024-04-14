from core.rabbitmq.messages.base_request import BaseMessage

REMOVE_TOKENS_REQUEST_MESSAGE_TYPE = 'remove_tokens_request'
REMOVE_TOKENS_REQUEST_IDS = 'ids'


class RemoveTokensRequest(BaseMessage):

    def __init__(self, ids: list[int]):
        super().__init__(REMOVE_TOKENS_REQUEST_MESSAGE_TYPE)
        self.ids = ids

    def serialize(self):
        return self.to_json({
            REMOVE_TOKENS_REQUEST_IDS: self.ids
        })

    @staticmethod
    def deserialize(payload):
        ids = payload[REMOVE_TOKENS_REQUEST_IDS]
        return RemoveTokensRequest(ids)
