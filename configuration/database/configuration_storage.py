import os

from modules.core.log_service.log_service import Logger_Service
from modules.core.rabbitmq.messages.configuration.category_model import CategoryModel
from modules.core.rabbitmq.messages.configuration.credentials.credential_model import CredentialModel
from modules.core.rabbitmq.messages.configuration.token_model import TokenModel
from modules.core.rabbitmq.messages.configuration.url_model import UrlModel
from modules.core.sqlite.base_storage import BaseStorage

DATABASE_NAME = 'configuration_storage.db'

# ----- Credentials table -----
CREDENTIALS_TABLE_NAME = 'credentials'
CREDENTIALS_LOGIN_COLUMN_NAME = 'login'
CREDENTIALS_DOMAIN_COLUMN_NAME = 'domain'
CREDENTIALS_EMAIL_COLUMN_NAME = 'email'
CREDENTIALS_PASSWORD_COLUMN_NAME = 'pass'
# ------------------------------

# ----- Urls table -----
URLS_TABLE_NAME = 'urls'
URLS_KEY_COLUMN_NAME = 'key'
URLS_VALUE_COLUMN_NAME = 'value'
# ------------------------------

# ----- Meeting categories ------
MEETING_CATEGORIES_TABLE_NAME = 'meeting_categories'
MEETING_CATEGORIES_NAME_COLUMN_NAME = 'name'
MEETING_CATEGORIES_TRACKER_ID_COLUMN_NAME = 'tracker_id'
MEETING_CATEGORIES_LINK_COLUMN_NAME = 'link'
# ------------------------------

# ----- Todoist categories ------
TODOIST_LABELS_TABLE_NAME = 'todoist_labels'
TODOIST_CATEGORIES_NAME_COLUMN_NAME = 'name'
TODOIST_CATEGORIES_TRACKER_ID_COLUMN_NAME = 'tracker_id'
TODOIST_CATEGORIES_LINK_COLUMN_NAME = 'link'
# ------------------------------

# ----- Tokens ------
TOKENS_TABLE_NAME = 'tokens'
TOKENS_NAME_COLUMN_NAME = 'name'
TOKENS_KEY_COLUMN_NAME = 'key'
# ------------------------------


class ConfigurationStorage(BaseStorage):
    def __init__(self, path: str, logger: Logger_Service):
        super().__init__(logger, os.path.join(path, DATABASE_NAME))

    def get_create_table_request(self) -> list[str]:
        credentials_table = f'''CREATE TABLE IF NOT EXISTS {CREDENTIALS_TABLE_NAME} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                {CREDENTIALS_LOGIN_COLUMN_NAME} TEXT NOT NULL,
                                {CREDENTIALS_DOMAIN_COLUMN_NAME} TEXT NOT NULL,
                                {CREDENTIALS_EMAIL_COLUMN_NAME} TEXT NOT NULL,
                                {CREDENTIALS_PASSWORD_COLUMN_NAME} TEXT NOT NULL);'''

        urls_table = f'''CREATE TABLE IF NOT EXISTS {URLS_TABLE_NAME} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                {URLS_KEY_COLUMN_NAME} TEXT NOT NULL,
                                {URLS_VALUE_COLUMN_NAME} TEXT NULL);'''

        meeting_categories_table = f'''CREATE TABLE IF NOT EXISTS {MEETING_CATEGORIES_TABLE_NAME} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                {MEETING_CATEGORIES_NAME_COLUMN_NAME} TEXT NOT NULL,
                                {MEETING_CATEGORIES_TRACKER_ID_COLUMN_NAME} TEXT NOT NULL,
                                {MEETING_CATEGORIES_LINK_COLUMN_NAME} TEXT NULL);'''

        todoist_categories_table = f'''CREATE TABLE IF NOT EXISTS {TODOIST_LABELS_TABLE_NAME} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                {TODOIST_CATEGORIES_NAME_COLUMN_NAME} TEXT NOT NULL,
                                {TODOIST_CATEGORIES_TRACKER_ID_COLUMN_NAME} TEXT NOT NULL,
                                {TODOIST_CATEGORIES_LINK_COLUMN_NAME} TEXT NULL);'''

        tokens_table = f'''CREATE TABLE IF NOT EXISTS {TOKENS_TABLE_NAME} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                {TOKENS_NAME_COLUMN_NAME} TEXT NOT NULL,
                                {TOKENS_KEY_COLUMN_NAME} TEXT NOT NULL);'''

        return [credentials_table, urls_table, meeting_categories_table, todoist_categories_table, tokens_table]

    def get_credentials(self) -> CredentialModel:
        sqlite_select_query = f'SELECT {CREDENTIALS_LOGIN_COLUMN_NAME}, {CREDENTIALS_EMAIL_COLUMN_NAME}, {CREDENTIALS_DOMAIN_COLUMN_NAME}, {CREDENTIALS_PASSWORD_COLUMN_NAME} '
        sqlite_select_query += f'from {CREDENTIALS_TABLE_NAME} '
        sqlite_select_query += f'ORDER BY id DESC LIMIT {1}'

        result = self.get_first(sqlite_select_query)
        if result is None:
            raise Exception('Can not find credentials')

        login = result[0]
        email = result[1]
        domain = result[2]
        password = result[3]

        return CredentialModel(login, email, domain, password)

    def get_meeting_categories(self) -> list[CategoryModel]:
        query = f'''SELECT {MEETING_CATEGORIES_NAME_COLUMN_NAME}, {MEETING_CATEGORIES_TRACKER_ID_COLUMN_NAME}, {MEETING_CATEGORIES_LINK_COLUMN_NAME} from {MEETING_CATEGORIES_TABLE_NAME}'''
        data = self.get_data(query)
        models = []
        for row in data:

            models.append(CategoryModel(row[0], row[1], row[2]))
        return models

    def set_meeting_categories(self, categories: list[CategoryModel]):
        query = f'DELETE FROM {MEETING_CATEGORIES_TABLE_NAME}'
        self.remove(query)
        for category in categories:
            query = f'''INSERT INTO {MEETING_CATEGORIES_TABLE_NAME} 
                ({MEETING_CATEGORIES_NAME_COLUMN_NAME}, {MEETING_CATEGORIES_TRACKER_ID_COLUMN_NAME}, {MEETING_CATEGORIES_LINK_COLUMN_NAME})
                VALUES
                (:{MEETING_CATEGORIES_NAME_COLUMN_NAME}, :{MEETING_CATEGORIES_TRACKER_ID_COLUMN_NAME}, :{MEETING_CATEGORIES_LINK_COLUMN_NAME})
            '''

            params = {
                MEETING_CATEGORIES_NAME_COLUMN_NAME: category.name,
                MEETING_CATEGORIES_TRACKER_ID_COLUMN_NAME: category.tracker_id,
                MEETING_CATEGORIES_LINK_COLUMN_NAME: category.link,
            }

            self.insert(query, params)

    def get_task_categories(self) -> list[CategoryModel]:
        query = f'''SELECT {TODOIST_CATEGORIES_NAME_COLUMN_NAME}, {TODOIST_CATEGORIES_TRACKER_ID_COLUMN_NAME}, {TODOIST_CATEGORIES_LINK_COLUMN_NAME} from {TODOIST_LABELS_TABLE_NAME}'''
        data = self.get_data(query)
        models = []
        for row in data:

            models.append(CategoryModel(row[0], row[1], row[2]))
        return models

    def set_task_categories(self, categories: list[CategoryModel]):
        query = f'DELETE FROM {TODOIST_LABELS_TABLE_NAME}'
        self.remove(query)
        for category in categories:
            query = f'''INSERT INTO {TODOIST_LABELS_TABLE_NAME} 
                ({TODOIST_CATEGORIES_NAME_COLUMN_NAME}, {TODOIST_CATEGORIES_TRACKER_ID_COLUMN_NAME}, {TODOIST_CATEGORIES_LINK_COLUMN_NAME})
                VALUES
                (:{TODOIST_CATEGORIES_NAME_COLUMN_NAME}, :{TODOIST_CATEGORIES_TRACKER_ID_COLUMN_NAME}, :{TODOIST_CATEGORIES_LINK_COLUMN_NAME})
            '''

            params = {
                TODOIST_CATEGORIES_NAME_COLUMN_NAME: category.name,
                TODOIST_CATEGORIES_TRACKER_ID_COLUMN_NAME: category.tracker_id,
                TODOIST_CATEGORIES_LINK_COLUMN_NAME: category.link,
            }

            self.insert(query, params)

    def get_tokens(self) -> list[TokenModel]:
        query = f'''SELECT {TOKENS_NAME_COLUMN_NAME}, {TOKENS_KEY_COLUMN_NAME} from {TOKENS_TABLE_NAME}'''
        data = self.get_data(query)
        models = []
        for row in data:
            models.append(TokenModel(row[0], row[1]))
        return models

    def set_tokens(self, categories: list[TokenModel]):
        query = f'DELETE FROM {TOKENS_TABLE_NAME}'
        self.remove(query)
        for category in categories:
            query = f'''INSERT INTO {TOKENS_TABLE_NAME} 
                    ({TOKENS_NAME_COLUMN_NAME}, {TOKENS_KEY_COLUMN_NAME})
                    VALUES
                    (:{TOKENS_NAME_COLUMN_NAME}, :{TOKENS_KEY_COLUMN_NAME})
                '''

            params = {
                TOKENS_NAME_COLUMN_NAME: category.name,
                TOKENS_KEY_COLUMN_NAME: category.key,
            }

            self.insert(query, params)

    def get_urls(self) -> list[UrlModel]:
        query = f'''SELECT {TOKENS_NAME_COLUMN_NAME}, {TOKENS_KEY_COLUMN_NAME} from {TOKENS_TABLE_NAME}'''
        data = self.get_data(query)
        models = []
        for row in data:
            models.append(UrlModel(row[0], row[1]))
        return models


    def get_url(self, url_type: str):
        query = f'''SELECT {URLS_VALUE_COLUMN_NAME} from {URLS_TABLE_NAME} 
         where {URLS_KEY_COLUMN_NAME} = "{url_type}"
         ORDER BY id DESC LIMIT {1}
        '''
        result = self.get_first(query)
        if result is None:
            raise Exception(f'Can not find url for {url_type}')

        return result[0]

    def set_urls(self, models: list[UrlModel]):
        query = f'DELETE FROM {URLS_TABLE_NAME}'
        self.remove(query)
        for url in models:
            query = f'''INSERT INTO {URLS_TABLE_NAME} 
                ({URLS_KEY_COLUMN_NAME}, {URLS_VALUE_COLUMN_NAME})
                VALUES
                (:{URLS_KEY_COLUMN_NAME}, :{URLS_VALUE_COLUMN_NAME})
            '''

            params = {
                TOKENS_NAME_COLUMN_NAME: url.name,
                TOKENS_KEY_COLUMN_NAME: url.key,
            }

            self.insert(query, params)

    def set_credentials(self, credentials: CredentialModel):
        query = f'DELETE FROM {CREDENTIALS_TABLE_NAME}'
        self.remove(query)

        query = f'''INSERT INTO {CREDENTIALS_TABLE_NAME} 
                ({CREDENTIALS_LOGIN_COLUMN_NAME}, {CREDENTIALS_DOMAIN_COLUMN_NAME}, {CREDENTIALS_EMAIL_COLUMN_NAME}, {CREDENTIALS_PASSWORD_COLUMN_NAME})
                VALUES
                (:{CREDENTIALS_LOGIN_COLUMN_NAME}, :{CREDENTIALS_DOMAIN_COLUMN_NAME}, :{CREDENTIALS_EMAIL_COLUMN_NAME}, :{CREDENTIALS_PASSWORD_COLUMN_NAME})
            '''

        params = {
            CREDENTIALS_LOGIN_COLUMN_NAME: credentials.login,
            CREDENTIALS_DOMAIN_COLUMN_NAME: credentials.domain,
            CREDENTIALS_EMAIL_COLUMN_NAME: credentials.email,
            CREDENTIALS_PASSWORD_COLUMN_NAME: credentials.password,
        }

        self.insert(query, params)
