IPTV_SOURCE_MODEL_VALUE = 'value'
IPTV_SOURCE_MODEL_ID = 'id'


class IptvSourceModel:
    def __init__(self, id: int, value: str):
        self.id = id
        self.value = value

    def serialize(self) -> dict:
        return {
            IPTV_SOURCE_MODEL_ID: self.id,
            IPTV_SOURCE_MODEL_VALUE: self.value,
        }

    @staticmethod
    def deserialize(payload):
        id = payload[IPTV_SOURCE_MODEL_ID]
        value = payload[IPTV_SOURCE_MODEL_VALUE]
        return IptvSourceModel(id, value)
