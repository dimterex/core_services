from web_host.messages.base_response import BaseResponse


class MeetingCategoriesResponse(BaseResponse):
    def __init__(self, status: str, categories: list[dict] = None, exception: str = None):
        super().__init__(status, exception)
        self.categories = categories
        self.exception = exception
        self.status = status

    def serialize(self) -> dict:
        return {
            'status': self.status,
            'categories': self.categories,
            'exception': self.exception,
        }
