from web_host.messages.base_response import BaseResponse


class TokensResponse(BaseResponse):
    def __init__(self, status: str, tokens: list[dict] = None, exception: str = None):
        super().__init__(status, exception)
        self.tokens = tokens
        self.exception = exception
        self.status = status

    def serialize(self) -> dict:
        return {
            'status': self.status,
            'tokens': self.tokens,
            'exception': self.exception,
        }
