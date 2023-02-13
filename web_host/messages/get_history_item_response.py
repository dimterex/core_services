from web_host.messages.base_response import BaseResponse


class HistoryItemResponse(BaseResponse):
    def __init__(self, status: str, messages: list[str] = None, exception: str = None):
        super().__init__(status, exception)
        self.messages = messages

    def serialize(self) -> dict:
        return {
            'status': self.status,
            'messages': self.messages,
            'exception': self.exception,
        }
