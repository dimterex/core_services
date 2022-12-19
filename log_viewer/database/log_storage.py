import os
import sqlite3

from log_viewer.messages.LogModel import LogModel
from modules.core.log_service.log_service import Logger_Service
from modules.core.sqlite.base_storage import BaseStorage

LOG_DATABASE_NAME = 'log_storage.db'
TABLE_NAME = 'messages'
MESSAGE_COLUMN_NAME = 'message'
LEVEL_COLUMN_NAME = 'level'
TAG_COLUMN_NAME = 'tag'
APPLICATION_COLUMN_NAME = 'application'
DATATIME_COLUMN_NAME = 'datatime'


class Log_Storage(BaseStorage):
    def __init__(self, path: str, logger: Logger_Service):
        super().__init__(logger, os.path.join(path, LOG_DATABASE_NAME))

    def get_create_table_request(self) -> str:
        return f'''CREATE TABLE {TABLE_NAME} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                {MESSAGE_COLUMN_NAME} TEXT NOT NULL,
                                {LEVEL_COLUMN_NAME} TEXT NOT NULL,
                                {TAG_COLUMN_NAME} TEXT NOT NULL,
                                {APPLICATION_COLUMN_NAME} TEXT NOT NULL,
                                {DATATIME_COLUMN_NAME} TEXT NOT NULL);'''

    def add_log(self, log_model: LogModel):
        try:
            sqlite_connection = sqlite3.connect(self.path)
            cursor = sqlite_connection.cursor()

            sqlite_insert_query = f'INSERT INTO {TABLE_NAME} '
            sqlite_insert_query += f'({MESSAGE_COLUMN_NAME}, {LEVEL_COLUMN_NAME}, {TAG_COLUMN_NAME}, {APPLICATION_COLUMN_NAME}, {DATATIME_COLUMN_NAME}) '
            sqlite_insert_query += f'VALUES '
            sqlite_insert_query += f'(:{MESSAGE_COLUMN_NAME}, :{LEVEL_COLUMN_NAME}, :{TAG_COLUMN_NAME}, :{APPLICATION_COLUMN_NAME}, :{DATATIME_COLUMN_NAME})'

            cursor.execute(sqlite_insert_query, {
                f'{MESSAGE_COLUMN_NAME}': log_model.message,
                f'{LEVEL_COLUMN_NAME}': log_model.level,
                f'{TAG_COLUMN_NAME}': log_model.tag,
                f'{APPLICATION_COLUMN_NAME}': log_model.applicationName,
                f'{DATATIME_COLUMN_NAME}': log_model.datetime,
            })
            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def read_limited_rows(self, application_name: str, row_count: int) -> list[LogModel]:
        try:
            sqlite_connection = sqlite3.connect(self.path)
            cursor = sqlite_connection.cursor()

            sqlite_select_query = f'SELECT {APPLICATION_COLUMN_NAME}, {TAG_COLUMN_NAME},{LEVEL_COLUMN_NAME}, {DATATIME_COLUMN_NAME}, {MESSAGE_COLUMN_NAME} '
            sqlite_select_query += f'from {TABLE_NAME} '
            sqlite_select_query += f'where {APPLICATION_COLUMN_NAME} = "{application_name}" '
            sqlite_select_query += f'ORDER BY id DESC LIMIT {row_count} '
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            log_models = []
            for row in records:
                # applicationName, tag, level, datetime, message
                log_models.append(LogModel(row[0], row[1], row[2], row[3], row[4]))
            cursor.close()
            return log_models

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite: ", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def get_applications(self):
        try:
            sqlite_connection = sqlite3.connect(self.path)
            cursor = sqlite_connection.cursor()

            sqlite_select_query = f'''SELECT DISTINCT {APPLICATION_COLUMN_NAME} from {TABLE_NAME}'''
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            log_models = []
            for row in records:
                log_models.append(row[0])
            cursor.close()
            return log_models

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite: ", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

