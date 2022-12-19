from web_host.messages.base_response import BaseResponse


class MonthTimesResponse(BaseResponse):
    def __init__(self, status: str, messages: list[str] = None, exception: str = None):
        super().__init__(status, exception)
        self.messages = messages
        self.exception = exception
        self.status = status

    def toJson(self) -> dict:
        return {
            'status': self.status,
            'messages': self.messages,
            'exception': self.exception,
        }