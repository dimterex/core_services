from core.http_server.base_response import BaseResponse


class SetBaseResponse(BaseResponse):
    def __init__(self, status: str, exception: str = None):
        super().__init__(status, exception)

    def serialize(self) -> dict:
        return {
            'status': self.status,
            'message': self.exception,
        }
