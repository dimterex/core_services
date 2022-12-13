class BaseResponse:
    def __init__(self, status: str, exception: str = None):
        self.exception = exception
        self.status = status

    def toJson(self) -> dict:
        raise Exception('Not implemented')
