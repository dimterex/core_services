IPTV_EPG_SOURCE_MODEL_VALUE = 'value'
IPTV_EPG_SOURCE_MODEL_ID = 'id'


class IptvEpgSourceModel:
    def __init__(self, id: int, value: str):
        self.id = id
        self.value = value

    def serialize(self) -> dict:
        return {
            IPTV_EPG_SOURCE_MODEL_ID: self.id,
            IPTV_EPG_SOURCE_MODEL_VALUE: self.value,
        }

    @staticmethod
    def deserialize(payload):
        id = payload[IPTV_EPG_SOURCE_MODEL_ID]
        value = payload[IPTV_EPG_SOURCE_MODEL_VALUE]
        return IptvEpgSourceModel(id, value)
