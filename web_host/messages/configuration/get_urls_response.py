from web_host.messages.base_response import BaseResponse


class UrlsResponse(BaseResponse):
    def __init__(self, status: str, urls: list[dict] = None, exception: str = None):
        super().__init__(status, exception)
        self.urls = urls
        self.exception = exception
        self.status = status

    def toJson(self) -> dict:
        return {
            'status': self.status,
            'urls': self.urls,
            'exception': self.exception,
        }
