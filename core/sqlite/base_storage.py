import sqlite3

from core.log_service.log_service import Logger_Service


class BaseStorage:
    def __init__(self, logger: Logger_Service, path: str):
        self.path = path
        self.logger = logger
        self.TAG = self.__class__.__name__
        self.create_database()

    def get_create_table_request(self) -> list[str]:
        raise Exception('Not implemented')

    def create_database(self):
        sqlite_connection = None
        try:
            sqlite_connection = sqlite3.connect(self.path)
            cursor = sqlite_connection.cursor()
            for script in self.get_create_table_request():
                cursor.execute(script)
            sqlite_connection.commit()
        except Exception as e:
            self.logger.error(self.TAG, str(e))
        finally:
            if sqlite_connection:
                sqlite_connection.close()
