from core.rabbitmq.messages.base_request import BaseMessage

REMOVE_IPTV_BLACK_LIST_ITEM_REQUEST_MESSAGE_TYPE = 'remove_black_list_item_request'
REMOVE_IPTV_BLACK_LIST_ITEM_REQUEST_ID = 'id'


class RemoveBlackListItemRequest(BaseMessage):

    def __init__(self, id: int):
        super().__init__(REMOVE_IPTV_BLACK_LIST_ITEM_REQUEST_ID)
        self.id = id

    def serialize(self):
        return self.to_json({
            REMOVE_IPTV_BLACK_LIST_ITEM_REQUEST_ID: self.id
        })

    @staticmethod
    def deserialize(payload):
        id = payload[REMOVE_IPTV_BLACK_LIST_ITEM_REQUEST_ID]
        return RemoveBlackListItemRequest(id)
