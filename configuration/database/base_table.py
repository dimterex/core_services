import sqlite3

from modules.core.log_service.log_service import Logger_Service


class BaseTable:

    def __init__(self, table_name: str, id_column: str, logger: Logger_Service, path: str):
        self.id_column = id_column
        self.table_name = table_name
        self.path = path
        self.logger = logger
        self.TAG = self.__class__.__name__

    def get_initialize_table(self):
        raise Exception("Not implemented.")

    def get_first(self, params: dict[str, any]) -> any:
        sqlite_connection = None

        where_string = []
        for obj in params:
            where_string.append(f'{obj} = "{params[obj]}"')

        query = f'SELECT * from {self.table_name} where {"and ".join(where_string)} ORDER BY id DESC LIMIT {1}'
        try:
            sqlite_connection = sqlite3.connect(self.path)
            cursor = sqlite_connection.cursor()

            cursor.execute(query)
            records = cursor.fetchone()
            return records
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                self.logger.info(self.TAG, "Соединение с SQLite закрыто")

    def insert(self, params: dict) -> any:
        sqlite_connection = None
        id = None

        columns = []
        args = []
        keysList = list(params)

        for key in keysList:
            args.append(f'"{params[key]}"')
            columns.append(f'{key}')

        query = f'INSERT INTO {self.table_name} ({", ".join(columns)}) VALUES ({", ".join(args)})'

        try:
            sqlite_connection = sqlite3.connect(self.path)
            cursor = sqlite_connection.cursor()
            cursor.execute(query)
            sqlite_connection.commit()
            id = cursor.lastrowid
            cursor.close()
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                self.logger.info(self.TAG, "Соединение с SQLite закрыто")
            return id

    def update(self, params: dict[int, dict]) -> any:
        sqlite_connection = None

        try:
            sqlite_connection = sqlite3.connect(self.path)
            cursor = sqlite_connection.cursor()
            for row in params:
                obj = params[row]
                keysList = list(obj)

                set_string = []
                for key in keysList:
                    set_string.append(f'{key} = "{obj[key]}"')

                query = f'UPDATE {self.table_name} SET {", ".join(set_string)} where {self.id_column} = {row}'

                cursor.execute(query)
                sqlite_connection.commit()
            cursor.close()
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                self.logger.info(self.TAG, "Соединение с SQLite закрыто")

    def remove(self, ids: list[int]):
        sqlite_connection = None

        try:
            sqlite_connection = sqlite3.connect(self.path)
            cursor = sqlite_connection.cursor()
            for id in ids:
                query = f'DELETE from {self.table_name} where {self.id_column} = "{id}"'
                cursor.execute(query)
                sqlite_connection.commit()
            cursor.close()
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                self.logger.info(self.TAG, "Соединение с SQLite закрыто")

    def get_data(self):
        sqlite_connection = None
        query = f'SELECT * from {self.table_name}'
        try:
            sqlite_connection = sqlite3.connect(self.path)
            cursor = sqlite_connection.cursor()

            cursor.execute(query)
            records = cursor.fetchall()
            return records
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                self.logger.info(self.TAG, "Соединение с SQLite закрыто")
