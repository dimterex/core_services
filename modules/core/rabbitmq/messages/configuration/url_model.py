URL_MODEL_NAME = 'name'
URL_MODEL_VALUE = 'value'


class UrlModel:
    def __init__(self, name: str, value: str):
        self.name = name
        self.key = value

    def serialize(self) -> dict:
        return {
            URL_MODEL_NAME: self.name,
            URL_MODEL_VALUE: self.key,
        }

    @staticmethod
    def deserialize(payload):
        name = payload[URL_MODEL_NAME]
        key = payload[URL_MODEL_VALUE]
        return UrlModel(name, key)

