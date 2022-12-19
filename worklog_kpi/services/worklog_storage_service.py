import datetime
import os

import sqlite3

from modules.core.log_service.log_service import Logger_Service, ERROR_LOG_LEVEL
from worklog_kpi.models.worklog_sqlite_model import WorklogSqliteModel

WORKLOG_DATABASE_NAME = 'wokrlog_kpi.sqlite'

TABLE_NAME = 'history'
DESCRIPTION_COLUMN_NAME = 'description'
DATE_COLUMN_NAME = 'date'
ID_COLUMN_NAME = 'id'


class WorklogStorageService:

    def __init__(self, path: str, logger: Logger_Service):
        self.logger = logger
        self.path = os.path.join(path, WORKLOG_DATABASE_NAME)
        self.create_database()
        self.TAG = self.__class__.__name__

    def create_database(self):
        try:
            sqlite_connection = sqlite3.connect(self.path)
            cursor = sqlite_connection.cursor()
            cursor.close()
            sqlite_create_table_query = f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                                {ID_COLUMN_NAME} INTEGER PRIMARY KEY AUTOINCREMENT,
                                {DESCRIPTION_COLUMN_NAME} TEXT NULL,
                                {DATE_COLUMN_NAME} TEXT NOT NULL);'''
            cursor = sqlite_connection.cursor()
            cursor.execute(sqlite_create_table_query)
            sqlite_connection.commit()
        except Exception as e:
            self.logger.error(self.TAG, str(e))
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    def add(self, model: WorklogSqliteModel):
        try:
            sqlite_connection = sqlite3.connect(self.path)
            cursor = sqlite_connection.cursor()

            sqlite_insert_query = f'INSERT INTO {TABLE_NAME} '
            sqlite_insert_query += f'({DATE_COLUMN_NAME}, {DESCRIPTION_COLUMN_NAME}) '
            sqlite_insert_query += f'VALUES '
            sqlite_insert_query += f'(:{DATE_COLUMN_NAME}, :{DESCRIPTION_COLUMN_NAME})'

            cursor.execute(sqlite_insert_query, {
                f'{DATE_COLUMN_NAME}': model.date,
                f'{DESCRIPTION_COLUMN_NAME}': model.description,
            })
            sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            self.logger.error(self.TAG, str(error))
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    def get_by_date(self, date: datetime.date) -> list[WorklogSqliteModel]:
        try:
            sqlite_connection = sqlite3.connect(self.path)
            cursor = sqlite_connection.cursor()
            result: list[WorklogSqliteModel] = []

            sqlite_select_query = f'SELECT {DESCRIPTION_COLUMN_NAME} '
            sqlite_select_query += f'from {TABLE_NAME} '
            sqlite_select_query += f'where {DATE_COLUMN_NAME} = "{date}" '
            for row in cursor.execute(sqlite_select_query):
                result.append(WorklogSqliteModel(str(date), row))
            cursor.close()
            return result
        except sqlite3.Error as error:
            self.logger.error(self.TAG, str(error))
        finally:
            if sqlite_connection:
                sqlite_connection.close()
