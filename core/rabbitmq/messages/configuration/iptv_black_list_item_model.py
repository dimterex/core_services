IPTV_BLACK_LIST_ITEM_MODEL_TYPE = 'type'
IPTV_BLACK_LIST_ITEM_MODEL_VALUE = 'value'
IPTV_BLACK_LIST_ITEM_MODEL_ID = 'id'

CHANNEL_TYPE = 'channel'
CATEGORY_TYPE = 'category'


class IptvBlackListItemModel:
    def __init__(self, id: int, value: str, type: str):
        self.id = id
        self.value = value
        self.type = type

    def serialize(self) -> dict:
        return {
            IPTV_BLACK_LIST_ITEM_MODEL_ID: self.id,
            IPTV_BLACK_LIST_ITEM_MODEL_VALUE: self.value,
            IPTV_BLACK_LIST_ITEM_MODEL_TYPE: self.type,
        }

    @staticmethod
    def deserialize(payload):
        id = payload[IPTV_BLACK_LIST_ITEM_MODEL_ID]
        value = payload[IPTV_BLACK_LIST_ITEM_MODEL_VALUE]
        type = payload[IPTV_BLACK_LIST_ITEM_MODEL_TYPE]
        return IptvBlackListItemModel(id, value, type)
