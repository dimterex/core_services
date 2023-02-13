TOKEN_MODEL_NAME = 'name'
TOKEN_MODEL_KEY = 'key'
TOKEN_MODEL_ID = 'id'


class TokenModel:
    def __init__(self, id: int, name: str, key: str):
        self.id = id
        self.name = name
        self.key = key

    def serialize(self) -> dict:
        return {
            TOKEN_MODEL_ID: self.id,
            TOKEN_MODEL_NAME: self.name,
            TOKEN_MODEL_KEY: self.key,
        }

    @staticmethod
    def deserialize(payload):
        id = payload[TOKEN_MODEL_ID]
        name = payload[TOKEN_MODEL_NAME]
        key = payload[TOKEN_MODEL_KEY]
        return TokenModel(id, name, key)
