IPTV_DUPLICATE_LIST_ITEM_MODEL_TYPE = 'type'
IPTV_DUPLICATE_LIST_ITEM_MODEL_OLD_VALUE = 'old_value'
IPTV_DUPLICATE_LIST_ITEM_MODEL_VALUE = 'value'
IPTV_DUPLICATE_LIST_ITEM_MODEL_ID = 'id'

CHANNEL_TYPE = 'channel'
CATEGORY_TYPE = 'category'
REGEX_TYPE = 'regex'


class IptvDuplicateListItemModel:
    def __init__(self, id: int, old_value: str, value: str, type: str):
        self.id = id
        self.old_value = old_value
        self.value = value
        self.type = type

    def serialize(self) -> dict:
        return {
            IPTV_DUPLICATE_LIST_ITEM_MODEL_ID: self.id,
            IPTV_DUPLICATE_LIST_ITEM_MODEL_OLD_VALUE: self.old_value,
            IPTV_DUPLICATE_LIST_ITEM_MODEL_VALUE: self.value,
            IPTV_DUPLICATE_LIST_ITEM_MODEL_TYPE: self.type,
        }

    @staticmethod
    def deserialize(payload):
        id = payload[IPTV_DUPLICATE_LIST_ITEM_MODEL_ID]
        old_value = payload[IPTV_DUPLICATE_LIST_ITEM_MODEL_OLD_VALUE]
        value = payload[IPTV_DUPLICATE_LIST_ITEM_MODEL_VALUE]
        type = payload[IPTV_DUPLICATE_LIST_ITEM_MODEL_TYPE]
        return IptvDuplicateListItemModel(id, old_value, value, type)
