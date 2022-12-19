from web_host.messages.base_response import BaseResponse


class SetBaseResponse(BaseResponse):
    def __init__(self, status: str, exception: str = None):
        super().__init__(status, exception)

    def toJson(self) -> dict:
        return {
            'status': self.status,
            'exception': self.exception,
        }
