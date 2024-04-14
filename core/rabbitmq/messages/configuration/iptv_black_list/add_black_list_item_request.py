from core.rabbitmq.messages.base_request import BaseMessage

ADD_BLACK_LIST_ITEM_REQUEST_MESSAGE_TYPE = 'add_black_list_item_request'
ADD_BLACK_LIST_ITEM_REQUEST_TRACK_NAME = 'name'

class AddBlackListItemRequest(BaseMessage):
    def __init__(self, value: str):
        super().__init__(ADD_BLACK_LIST_ITEM_REQUEST_MESSAGE_TYPE)
        self.value = value

    def serialize(self):
        return self.to_json({
            ADD_BLACK_LIST_ITEM_REQUEST_TRACK_NAME: self.value,
        })

    @staticmethod
    def deserialize(payload):
        value = payload[ADD_BLACK_LIST_ITEM_REQUEST_TRACK_NAME]
        return AddBlackListItemRequest(value)

