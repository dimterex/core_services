from log_viewer.database.log_storage import Log_Storage
from log_viewer.messages.LogModel import LogModel


class Log_Service:
    def __init__(self, log_storage: Log_Storage):
        self.log_storage = log_storage

    def add_log(self, logModel: LogModel):
        self.log_storage.add_log(logModel)

    def get_applications(self):
        return self.log_storage.get_applications()

    def get_logs_by_application(self, application: str):
        return self.log_storage.read_limited_rows(application, 100)
