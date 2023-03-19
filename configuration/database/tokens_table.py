from configuration.database.base_table import BaseTable
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.configuration.token_model import TokenModel

ID_COLUMN_NAME = 'id'

TOKENS_TABLE_NAME = 'tokens'
TOKENS_NAME_COLUMN_NAME = 'name'
TOKENS_KEY_COLUMN_NAME = 'key'


class TokensTable(BaseTable):
    def __init__(self, logger: Logger_Service, path: str):
        super().__init__(TOKENS_TABLE_NAME, ID_COLUMN_NAME, logger, path)

    def get_initialize_table(self):
        return f'''CREATE TABLE IF NOT EXISTS {TOKENS_TABLE_NAME} (
                                {ID_COLUMN_NAME} INTEGER PRIMARY KEY AUTOINCREMENT,
                                {TOKENS_NAME_COLUMN_NAME} TEXT NOT NULL,
                                {TOKENS_KEY_COLUMN_NAME} TEXT NOT NULL);'''

    def get_tokens(self) -> list[TokenModel]:
        data = self.get_data()
        models = []
        for row in data:
            models.append(TokenModel(row[0], row[1], row[2]))
        return models

    def get_token(self, key: str) -> str:
        result = self.get_first({
            TOKENS_NAME_COLUMN_NAME: key
        })
        if result is None:
            raise Exception(f'Can not find token for {key}')

        return result[2]

    def set_token(self, token: TokenModel):
        self.set_tokens([token])

    def set_tokens(self, tokens: list[TokenModel]):
        params:  dict[int, dict] = {}

        for token in tokens:
            params[token.id] = {
                TOKENS_NAME_COLUMN_NAME: token.name,
                TOKENS_KEY_COLUMN_NAME: token.key,
            }

        self.update(params)

    def add_new_token(self):
        return self.insert({
            TOKENS_NAME_COLUMN_NAME: str(),
            TOKENS_KEY_COLUMN_NAME: str(),
        })
