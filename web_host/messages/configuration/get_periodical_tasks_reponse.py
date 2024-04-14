from core.http_server.base_response import BaseResponse


class PeriodicalTasksResponse(BaseResponse):
    def __init__(self, status: str, tasks: list[dict] = None, exception: str = None):
        super().__init__(status, exception)
        self.tasks = tasks

    def serialize(self) -> dict:
        return {
            'status': self.status,
            'tasks': self.tasks,
            'exception': self.exception,
        }
