TOKEN_MODEL_NAME = 'name'
TOKEN_MODEL_KEY = 'key'


class TokenModel:
    def __init__(self, name: str, key: str):
        self.name = name
        self.key = key

    def serialize(self) -> dict:
        return {
            TOKEN_MODEL_NAME: self.name,
            TOKEN_MODEL_KEY: self.key,
        }

    @staticmethod
    def deserialize(payload):
        name = payload[TOKEN_MODEL_NAME]
        key = payload[TOKEN_MODEL_KEY]
        return TokenModel(name, key)

