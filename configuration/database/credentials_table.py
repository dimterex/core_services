from configuration.database.base_table import BaseTable
from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.configuration.credentials.credential_model import CredentialModel

ID_COLUMN_NAME = "id"

CREDENTIALS_TABLE_NAME = 'credentials'
CREDENTIALS_LOGIN_COLUMN_NAME = 'login'
CREDENTIALS_DOMAIN_COLUMN_NAME = 'domain'
CREDENTIALS_EMAIL_COLUMN_NAME = 'email'
CREDENTIALS_PASSWORD_COLUMN_NAME = 'pass'

DEFAULT_CREDENTIALS_ID = 1


class CredentialsTable(BaseTable):
    def __init__(self, logger: Logger_Service, path: str):
        super().__init__(CREDENTIALS_TABLE_NAME, ID_COLUMN_NAME, logger, path)

    def get_initialize_table(self):
        return f'''CREATE TABLE IF NOT EXISTS {CREDENTIALS_TABLE_NAME} (
                                {ID_COLUMN_NAME} INTEGER PRIMARY KEY AUTOINCREMENT,
                                {CREDENTIALS_LOGIN_COLUMN_NAME} TEXT NOT NULL,
                                {CREDENTIALS_DOMAIN_COLUMN_NAME} TEXT NOT NULL,
                                {CREDENTIALS_EMAIL_COLUMN_NAME} TEXT NOT NULL,
                                {CREDENTIALS_PASSWORD_COLUMN_NAME} TEXT NOT NULL);'''

    def get_credentials(self) -> CredentialModel:
        result = self.get_first({
            ID_COLUMN_NAME: DEFAULT_CREDENTIALS_ID
        })
        if result is None:
            raise Exception('Can not find credentials')

        login = result[1]
        email = result[3]
        domain = result[2]
        password = result[4]

        return CredentialModel(login, email, domain, password)

    def set_credentials(self, credentials: CredentialModel):
        params: dict[int, dict] = { DEFAULT_CREDENTIALS_ID: {
            CREDENTIALS_LOGIN_COLUMN_NAME: credentials.login,
            CREDENTIALS_DOMAIN_COLUMN_NAME: credentials.domain,
            CREDENTIALS_EMAIL_COLUMN_NAME: credentials.email,
            CREDENTIALS_PASSWORD_COLUMN_NAME: credentials.password,
        }}

        self.update(params)
