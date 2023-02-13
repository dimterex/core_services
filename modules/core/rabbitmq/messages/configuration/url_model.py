URL_MODEL_NAME = 'name'
URL_MODEL_VALUE = 'value'
URL_MODEL_ID = 'id'


class UrlModel:
    def __init__(self, id: int, name: str, value: str):
        self.id = id
        self.name = name
        self.key = value

    def serialize(self) -> dict:
        return {
            URL_MODEL_ID: self.id,
            URL_MODEL_NAME: self.name,
            URL_MODEL_VALUE: self.key,
        }

    @staticmethod
    def deserialize(payload):
        id = payload[URL_MODEL_ID]
        name = payload[URL_MODEL_NAME]
        key = payload[URL_MODEL_VALUE]
        return UrlModel(id, name, key)
