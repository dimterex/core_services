from core.http_server.base_response import BaseResponse


class UrlsResponse(BaseResponse):
    def __init__(self, status: str, urls: list[dict] = None, exception: str = None):
        super().__init__(status, exception)
        self.urls = urls

    def serialize(self) -> dict:
        return {
            'status': self.status,
            'urls': self.urls,
            'exception': self.exception,
        }
