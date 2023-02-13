class BaseResponse:
    def __init__(self, status: str, message: str = None):
        self.message = message
        self.status = status

    def serialize(self) -> dict:
        raise Exception('Not implemented')
