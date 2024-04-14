from core.http_server.base_response import BaseResponse


class SetWorklogResponse(BaseResponse):
    def __init__(self, status: str, message: str = None, exception: str = None):
        super().__init__(status, exception)
        self.message = message
        self.exception = exception
        self.status = status

    def serialize(self) -> dict:
        return {
            'status': self.status,
            'message': self.message,
            'exception': self.exception,
        }
